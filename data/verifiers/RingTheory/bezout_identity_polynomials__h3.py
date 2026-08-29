import sympy
from sympy import Poly, QQ, RR, CC, ZZ
from sympy.abc import x

def conditions(witness) -> list[bool]:
    try:
        F, f, g = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = bool(F.is_Field)
    except Exception:
        h1 = False
        
    try:
        Poly_f = Poly(f, x, domain=F)
        Poly_g = Poly(g, x, domain=F)
        h2 = True
    except Exception:
        h2 = False
        
    try:
        if not h2:
            neg_q = False
        else:
            gcd_fg = Poly_f.gcd(Poly_g)
            neg_q = bool(gcd_fg.is_zero or gcd_fg.degree() > 0)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f and g are polynomials over F",
    "¬Q: There do not exist polynomials a and b over F such that a*f + b*g = 1"
]

N_HYP = 2
NEG_Q_INDEX = 2