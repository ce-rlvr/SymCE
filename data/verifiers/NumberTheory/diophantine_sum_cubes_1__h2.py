import sympy
from sympy import Integer

def conditions(witness):
    try:
        if len(witness) != 2:
            return [False, False]
        x, y = witness
    except Exception:
        return [False, False]

    try:
        h1 = isinstance(x, (int, Integer)) and isinstance(y, (int, Integer))
    except Exception:
        h1 = False

    try:
        neg_q = (x, y) not in [(1, 0), (0, 1)]
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x and y are integers",
    "¬Q: (x,y) is not (1,0) or (0,1)"
]

N_HYP = 1
NEG_Q_INDEX = 1