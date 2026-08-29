import sympy
from sympy import symbols, Poly, QQ, ZZ, RR, CC

x = symbols('x')

def conditions(witness) -> list[bool]:
    try:
        F, f, g = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = bool(F.is_Field)
    except Exception:
        h1 = False
        
    try:
        f_poly = Poly(f, x, domain=F)
        g_poly = Poly(g, x, domain=F)
        h2 = True
    except Exception:
        h2 = False
        
    try:
        if h2:
            fg = f_poly.compose(g_poly)
            h3 = bool(fg.is_irreducible)
        else:
            h3 = False
    except Exception:
        h3 = False
        
    try:
        if h2:
            neg_q = not bool(f_poly.is_irreducible)
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = ["H_1: F is a field", "H_2: f and g are polynomials", "H_3: f composed with g is irreducible", "¬Q: f is not irreducible"]

N_HYP = 3
NEG_Q_INDEX = 3