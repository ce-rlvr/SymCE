import sympy
from sympy import fraction, Poly, diff
from sympy.abc import x, y, z

# Top-level setup
# We provide standard symbols and the field of rationals (QQ) for witness construction.
QQ = sympy.QQ
RR = sympy.RR
CC = sympy.CC

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: σ: K → K is a field homomorphism",
    "H_3: σ(a) = a for all elements a in F",
    "¬Q: σ is not a field automorphism of K"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the false conjecture.
    
    Expected witness format (dictionary):
    {
        'F': sympy.QQ,
        'K_type': 'rational_function_field',
        'K_gen': x,
        'sigma_K_gen': x**2  # The image of the generator under σ
    }
    """
    try:
        F = witness.get('F', None)
        K_type = witness.get('K_type', None)
        gen = witness.get('K_gen', None)
        sigma_gen = witness.get('sigma_K_gen', None)
        
        # H_1: F is a field
        h1 = False
        if F in [sympy.QQ, sympy.RR, sympy.CC]:
            h1 = True
        elif hasattr(F, 'is_Field') and F.is_Field:
            h1 = True
            
        # H_2: σ: K → K is a field homomorphism
        h2 = False
        sigma_gen_simp = None
        if K_type == 'rational_function_field' and gen is not None and sigma_gen is not None:
            sigma_gen_simp = sympy.cancel(sigma_gen)
            # A rational function substitution defines a valid field endomorphism of F(gen)
            # if and only if it is non-constant.
            if hasattr(sigma_gen_simp, 'free_symbols') and sigma_gen_simp.free_symbols.issubset({gen}):
                if diff(sigma_gen_simp, gen) != 0:
                    h2 = True
                    
        # H_3: σ(a) = a for all elements a in F
        h3 = False
        if h2:
            # The substitution map gen -> sigma_gen in F(gen) is an F-algebra homomorphism,
            # which by definition fixes the base field F pointwise.
            h3 = True
            
        # ¬Q: σ is not a field automorphism of K
        neg_q = False
        if h2 and sigma_gen_simp is not None:
            # By Lüroth's theorem, an endomorphism of F(gen) given by gen -> R(gen)
            # is an automorphism if and only if the rational function R has degree exactly 1.
            num, den = fraction(sigma_gen_simp)
            num_poly = Poly(num, gen)
            den_poly = Poly(den, gen)
            deg = max(num_poly.degree(), den_poly.degree())
            
            if deg > 1:
                neg_q = True
                
        return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        return [False, False, False, False]