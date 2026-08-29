import sympy
from sympy import minpoly, degree, Poly, QQ
from sympy.abc import x

def conditions(witness) -> list[bool]:
    try:
        F, alpha, f = witness
    except Exception:
        return [False, False, False, False]

    try:
        h1 = bool(getattr(F, 'is_Field', False) or (F == QQ))
    except Exception:
        h1 = False

    try:
        if F == QQ:
            mp = minpoly(alpha, x)
            h2 = (mp is not None) and (degree(mp, x) >= 1)
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        if F == QQ:
            mp = minpoly(alpha, x)
            p = Poly(f, x, domain=F)
            h3 = bool(p.degree() == degree(mp, x))
        else:
            h3 = False
    except Exception:
        h3 = False

    try:
        if F == QQ:
            mp = minpoly(alpha, x)
            p = Poly(f, x, domain=F)
            mp_poly = Poly(mp, x, domain=F)
            neg_q = bool(p != mp_poly)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: alpha is an algebraic element over F",
    "H_3: degree of f(x) equals the degree of F(alpha) over F",
    "not Q: f(x) is not the minimal polynomial of alpha over F"
]

N_HYP = 3
NEG_Q_INDEX = 3