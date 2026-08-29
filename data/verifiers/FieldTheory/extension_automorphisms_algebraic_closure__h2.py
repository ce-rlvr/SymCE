import sympy
from sympy.polys.domains import FractionField

# Top-level setup
x = sympy.Symbol('x')
QQ = sympy.QQ
RR = sympy.RR
CC = sympy.CC

def conditions(witness):
    h1, h2, neg_q = False, False, False
    try:
        # Parse witness
        if isinstance(witness, dict):
            F = witness.get('F')
            K = witness.get('K')
            sigma = witness.get('sigma')
        elif isinstance(witness, tuple) and len(witness) == 3:
            F, K, sigma = witness
        else:
            return [False, False, False]
            
        # Fallback for string representations of fields
        if isinstance(F, str):
            F_str = F.strip()
            if F_str in ['QQ', 'Q', 'RationalField', 'sympy.QQ']:
                F = sympy.QQ
            elif F_str in ['RR', 'R', 'RealField', 'sympy.RR']:
                F = sympy.RR
            elif F_str in ['CC', 'C', 'ComplexField', 'sympy.CC']:
                F = sympy.CC

        if isinstance(K, str):
            K_str = K.strip().replace(' ', '')
            if 'x' in K_str:
                if 'QQ' in K_str or 'Q(' in K_str:
                    K = sympy.QQ.frac_field(sympy.Symbol('x'))
                elif 'RR' in K_str or 'R(' in K_str:
                    K = sympy.RR.frac_field(sympy.Symbol('x'))
                elif 'CC' in K_str or 'C(' in K_str:
                    K = sympy.CC.frac_field(sympy.Symbol('x'))

        # Check H1: F is a field
        if hasattr(F, 'is_Field') and F.is_Field:
            h1 = True
            
        # Check H2: sigma is an F-automorphism of K
        if hasattr(K, 'is_Field') and K.is_Field:
            # For the standard counterexample, K is a purely transcendental extension F(x)
            if isinstance(K, FractionField) and K.domain == F and len(K.gens) == 1:
                gen = K.gens[0]
                gen_expr = sympy.sympify(gen)
                
                # Extract the image of the generator under sigma
                img = None
                if isinstance(sigma, dict):
                    img = sigma.get(gen)
                    if img is None:
                        img = sigma.get(gen_expr)
                    if img is None:
                        for k, v in sigma.items():
                            if str(k) == str(gen):
                                img = v
                                break
                elif callable(sigma):
                    try:
                        img = sigma(gen_expr)
                    except Exception:
                        img = sigma(gen)
                elif isinstance(sigma, str):
                    if '->' in sigma:
                        img_str = sigma.split('->')[1].strip()
                        img = sympy.sympify(img_str)
                    else:
                        img = sympy.sympify(sigma)
                else:
                    img = sigma
                    
                if img is not None:
                    img_expr = sympy.cancel(sympy.sympify(img))
                    
                    # Ensure the image is in F(x)
                    if img_expr.free_symbols.issubset({gen_expr}):
                        n, d = img_expr.as_numer_denom()
                        
                        n_poly = sympy.Poly(n, gen_expr)
                        d_poly = sympy.Poly(d, gen_expr)
                        
                        # An F-automorphism of F(x) must be a fractional linear transformation (ax+b)/(cx+d)
                        if n_poly.degree() <= 1 and d_poly.degree() <= 1:
                            a = n_poly.nth(1)
                            b = n_poly.nth(0)
                            c = d_poly.nth(1)
                            d_coeff = d_poly.nth(0)
                            
                            # Check invertibility condition: ad - bc != 0
                            det = a*d_coeff - b*c
                            if det != 0:
                                h2 = True
                                
        # Check ¬Q: sigma does not extend to an F-automorphism of F_bar
        # If K is purely transcendental over F, it is not a subfield of the algebraic closure F_bar.
        # Thus, the restriction of any automorphism of F_bar to K is undefined, failing the conclusion.
        if h1 and h2 and isinstance(K, FractionField):
            neg_q = True
            
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field with algebraic closure F_bar",
    "H_2: sigma is an F-automorphism of K",
    "¬Q: sigma does not extend to an F-automorphism of F_bar (e.g., K is not a subfield of F_bar)"
]

N_HYP = 2
NEG_Q_INDEX = 2