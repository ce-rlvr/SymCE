import sympy as sp
from sympy.abc import x

# Top-level setup
# K is implicitly Q (the rational numbers).
# The witness should be a dictionary with keys 'L', 'E1', 'E2'
# providing polynomials in x. For example:
# witness = {'L': x**3 - 2, 'E1': x, 'E2': x}

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: L is an extension field of K",
    "¬Q: E_1 \\cap E_2 is NOT a splitting field over K"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            L_poly = witness.get('L', None)
            E1_gen = witness.get('E1', None)
            E2_gen = witness.get('E2', None)
        else:
            witness = list(witness)
            if len(witness) != 3:
                return [False, False, False]
            L_poly, E1_gen, E2_gen = witness
            
        if L_poly is None or E1_gen is None or E2_gen is None:
            return [False, False, False]
            
    except Exception:
        return [False, False, False]
        
    # H1: K is a field. We use K = Q, which is always a field.
    h1 = True
    
    # H2: L is an extension field of K.
    try:
        l_poly_obj = sp.Poly(L_poly, x, domain='QQ')
        if l_poly_obj.degree() < 1 or l_poly_obj.degree() > 10:
            h2 = False
        else:
            h2 = l_poly_obj.is_irreducible
    except Exception:
        h2 = False
        
    # neg_Q: E1 \cap E2 is NOT a splitting field over K.
    try:
        if not h2:
            neg_q = False
        else:
            diff_poly = sp.Poly(E1_gen - E2_gen, x, domain='QQ')
            _, rem = diff_poly.div(l_poly_obj)
            
            if not rem.is_zero:
                # We only support the case where E1 and E2 are the same element
                # to trivially compute their intersection as E1.
                neg_q = False
            else:
                _, rem_e1 = sp.Poly(E1_gen, x, domain='QQ').div(l_poly_obj)
                e1_reduced = rem_e1.as_expr()
                
                r = sp.RootOf(L_poly, 0)
                e1_val = e1_reduced.subs(x, r)
                
                mpoly = sp.minpoly(e1_val, x)
                factored = sp.factor(mpoly, extension=e1_val)
                
                is_splitting = True
                if factored.is_Mul:
                    factors = factored.args
                else:
                    factors = [factored]
                    
                for f in factors:
                    if f.has(x):
                        if f.is_Pow:
                            base, exp = f.args
                            fp = sp.Poly(base, x)
                        else:
                            fp = sp.Poly(f, x)
                        if fp.degree() > 1:
                            is_splitting = False
                            break
                
                neg_q = not is_splitting
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]