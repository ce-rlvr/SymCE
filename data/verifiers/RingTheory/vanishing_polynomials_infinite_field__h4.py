import sympy
from sympy import Poly, QQ, ZZ, RR, CC
from sympy.abc import x, y, z

N_HYP = 3
NEG_Q_INDEX = 3

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: F contains infinitely many elements",
    "H_3: f is a polynomial over F",
    "not Q: f is not the zero polynomial"
]

def conditions(witness) -> list[bool]:
    w = witness
    
    if isinstance(w, tuple) and len(w) == 2:
        try:
            domain, expr = w
            w = Poly(expr, x, domain=domain)
        except Exception:
            pass

    try:
        if not isinstance(w, Poly):
            w = Poly(w, x, domain='QQ')
    except Exception:
        pass

    try:
        h1 = bool(w.domain.is_Field)
    except Exception:
        h1 = False

    try:
        h2 = bool(h1 and not str(w.domain).startswith('GF'))
    except Exception:
        h2 = False

    try:
        h3 = isinstance(w, Poly)
    except Exception:
        h3 = False

    try:
        neg_q = not w.is_zero
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]