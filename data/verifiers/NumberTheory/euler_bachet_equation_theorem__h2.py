import sympy
from sympy import Integer

def conditions(witness):
    try:
        x, y = witness
        h1 = isinstance(x, (int, Integer)) and isinstance(y, (int, Integer))
    except Exception:
        h1 = False

    try:
        x, y = witness
        allowed = [(-1, 0), (0, 1), (0, -1), (2, 3), (2, -3)]
        neg_q = (x, y) not in allowed
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: x and y are integers",
    "¬Q: (x, y) is not one of (-1, 0), (0, 1), (0, -1), (2, 3), or (2, -3)"
]

N_HYP = 1
NEG_Q_INDEX = 1