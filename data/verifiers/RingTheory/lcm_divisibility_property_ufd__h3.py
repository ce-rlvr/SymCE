import sympy
from sympy import lcm, div
from sympy.abc import x, y, z

def conditions(witness) -> list[bool]:
    try:
        a, b, c = witness
    except Exception:
        return [False, False, False, False]

    try:
        h1 = True
    except Exception:
        h1 = False

    try:
        h2 = hasattr(a, '__mul__') and hasattr(b, '__mul__') and hasattr(c, '__mul__')
    except Exception:
        h2 = False

    try:
        if isinstance(b, (int, sympy.Integer)) and isinstance(c, (int, sympy.Integer)):
            h3 = (c % b == 0)
        else:
            q, r = div(c, b)
            h3 = (r == 0)
    except Exception:
        h3 = False

    try:
        l = lcm(a, b)
        if isinstance(l, (int, sympy.Integer)) and isinstance(c, (int, sympy.Integer)):
            neg_q = (c % l != 0)
        else:
            q, r = div(c, l)
            neg_q = (r != 0)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: a, b, c are elements of R",
    "H_3: b divides c",
    "¬Q: lcm(a, b) does not divide c"
]

N_HYP = 3
NEG_Q_INDEX = 3