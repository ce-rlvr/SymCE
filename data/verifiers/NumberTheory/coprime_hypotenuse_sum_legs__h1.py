import sympy
from sympy import gcd
from sympy.abc import x, y, z

def conditions(witness):
    try:
        a, b, c = witness
    except Exception:
        return [False, False, False]

    try:
        diff = a**2 + b**2 - c**2
        if hasattr(diff, 'expand'):
            diff = diff.expand()
        h1 = bool(diff == 0)
    except Exception:
        h1 = False

    try:
        g1 = gcd(a, b)
        g2 = gcd(g1, c)
        h2 = bool(g2 == 1 or g2 == -1)
    except Exception:
        h2 = False

    try:
        g3 = gcd(c, a + b)
        neg_q = bool(g3 != 1 and g3 != -1)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a^2 + b^2 = c^2",
    "H_2: gcd(a, b, c) = 1",
    "¬Q: gcd(c, a + b) != 1"
]

N_HYP = 2
NEG_Q_INDEX = 2