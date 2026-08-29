import sympy
from sympy.ntheory import jacobi_symbol

def conditions(witness):
    try:
        n, a, b = witness
    except Exception:
        return [False, False, False, False]

    try:
        h1 = isinstance(n, (int, sympy.Integer)) and n > 0 and n % 2 == 1
    except Exception:
        h1 = False

    try:
        h2 = isinstance(a, (int, sympy.Integer))
    except Exception:
        h2 = False

    try:
        h3 = isinstance(b, (int, sympy.Integer))
    except Exception:
        h3 = False

    try:
        neg_q = jacobi_symbol(int(a), int(n)) != jacobi_symbol(int(b), int(n))
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: n is an odd positive integer",
    "H_2: a is an integer",
    "H_3: b is an integer",
    "¬Q: (a/n) != (b/n)"
]

N_HYP = 3
NEG_Q_INDEX = 3