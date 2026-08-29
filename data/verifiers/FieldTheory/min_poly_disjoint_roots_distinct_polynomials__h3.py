import sympy
from sympy import QQ, ZZ, I, sqrt, Dummy, minpoly, Poly

# Top-level setup
# F is expected to be a field like QQ.
# alpha and beta are expected to be algebraic elements over F.
# Example witness: (QQ, sqrt(2), -sqrt(2)) or (QQ, 1, 1)

def conditions(witness) -> list[bool]:
    try:
        F, alpha, beta = witness
    except Exception:
        return [False, False, False]
        
    # H_1: F is a field
    try:
        h1 = getattr(F, 'is_Field', False)
    except Exception:
        h1 = False
        
    # H_2: α and β are algebraic over F
    try:
        x = Dummy('x')
        p_alpha = minpoly(alpha, x, domain=F)
        p_beta = minpoly(beta, x, domain=F)
        if p_alpha is None or p_beta is None:
            h2 = False
        else:
            # Verify they are valid polynomials over F
            Poly(p_alpha, x, domain=F)
            Poly(p_beta, x, domain=F)
            h2 = True
    except Exception:
        h2 = False
        
    # ¬Q: The minimal polynomials of α and β over F have a common root in some extension field.
    # This is true if and only if their greatest common divisor in F[x] has degree >= 1.
    try:
        x = Dummy('x')
        p_alpha = minpoly(alpha, x, domain=F)
        p_beta = minpoly(beta, x, domain=F)
        poly_alpha = Poly(p_alpha, x, domain=F)
        poly_beta = Poly(p_beta, x, domain=F)
        common_poly = poly_alpha.gcd(poly_beta)
        neg_q = common_poly.degree() >= 1
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: α and β are algebraic over F",
    "¬Q: The minimal polynomials of α and β over F have a common root in some extension field"
]

N_HYP = 2
NEG_Q_INDEX = 2