import sympy
from sympy import cyclotomic_poly
from sympy.abc import x

def conditions(witness) -> list[bool]:
    try:
        n = int(witness)
        h1 = (n >= 3 and n == witness)
    except Exception:
        h1 = False

    try:
        n = int(witness)
        poly = cyclotomic_poly(n, x)
        val = poly.subs(x, -1)
        neg_q = (val != 1)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n >= 3 is an integer",
    "¬Q: Phi_n(-1) != 1"
]

N_HYP = 1
NEG_Q_INDEX = 1