import sympy
from sympy import Integer

def conditions(witness) -> list[bool]:
    try:
        x, y = witness
        h1_ok = isinstance(x, (int, Integer)) and isinstance(y, (int, Integer))
    except Exception:
        h1_ok = False

    try:
        x, y = witness
        neg_q_ok = tuple(witness) not in [(3, 5), (3, -5)]
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: x and y are integers",
    "¬Q: (x, y) is not (3, 5) and not (3, -5)"
]

N_HYP = 1
NEG_Q_INDEX = 1