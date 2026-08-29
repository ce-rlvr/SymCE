import sympy
from sympy import Integer

def conditions(witness) -> list[bool]:
    try:
        x, y = witness
    except Exception:
        return [False, False, False]

    # H_1: x, y \in \mathbb{Z}_{>0}
    try:
        h1 = bool(isinstance(x, (int, Integer)) and isinstance(y, (int, Integer)) and x > 0 and y > 0)
    except Exception:
        h1 = False

    # H_2: x < y
    try:
        h2 = bool(x < y)
    except Exception:
        h2 = False

    # ¬Q: not (x = 2 and y = 4)
    try:
        neg_q = not (x == 2 and y == 4)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: x, y are positive integers",
    "H_2: x < y",
    "¬Q: It is not the case that x = 2 and y = 4"
]

N_HYP = 2
NEG_Q_INDEX = 2