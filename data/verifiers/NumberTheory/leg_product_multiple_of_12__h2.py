import sympy
from sympy import Integer

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False, False]
        a, b, c = witness
    except Exception:
        return [False, False]

    # H_1: a, b, and c are strictly positive integers
    try:
        h1 = (isinstance(a, (int, Integer)) and 
              isinstance(b, (int, Integer)) and 
              isinstance(c, (int, Integer)) and 
              a > 0 and b > 0 and c > 0)
    except Exception:
        h1 = False

    # ¬Q: The product ab is not divisible by 12
    try:
        neg_q = (a * b) % 12 != 0
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: a, b, and c are strictly positive integers",
    "¬Q: The product ab is not divisible by 12"
]

N_HYP = 1
NEG_Q_INDEX = 1