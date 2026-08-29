import sympy
from sympy import I, pi, exp, totient, degree, minpoly
from sympy.abc import x

def conditions(witness):
    try:
        h1 = (isinstance(witness, int) or isinstance(witness, sympy.Integer)) and witness > 0
    except Exception:
        h1 = False

    try:
        if h1:
            n = int(witness)
            zeta = exp(2 * I * pi / n)
            mp = minpoly(zeta, x)
            deg = degree(mp, x)
            expected = totient(n)
            neg_q = bool(deg != expected)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "not Q: The degree of the field extension Q(zeta_n) over Q is not exactly phi(n)"
]

N_HYP = 1
NEG_Q_INDEX = 1