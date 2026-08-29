import sympy
from sympy import Poly, Symbol

x = Symbol('x')

def conditions(witness) -> list[bool]:
    try:
        f, g = witness
    except Exception:
        return [False, False, False]

    try:
        poly_f = Poly(f, x)
        h1_ok = True
    except Exception:
        h1_ok = False

    try:
        poly_g = Poly(g, x)
        h2_ok = True
    except Exception:
        h2_ok = False

    try:
        if h1_ok and h2_ok:
            neg_q_ok = bool(poly_g.is_zero)
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is a polynomial",
    "H_2: g is a polynomial",
    "¬Q: Unique q and r do not exist"
]

N_HYP = 2
NEG_Q_INDEX = 2