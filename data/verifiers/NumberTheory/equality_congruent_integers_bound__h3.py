import math
import sympy
from sympy import Integer

def conditions(witness) -> list[bool]:
    try:
        m, a, b = witness
    except Exception:
        return [False, False, False, False]

    # H_1: m is a positive integer
    try:
        h1 = isinstance(m, (int, Integer)) and not isinstance(m, bool) and m > 0
    except Exception:
        h1 = False

    # H_2: a and b are integers
    try:
        h2 = (isinstance(a, (int, Integer)) and not isinstance(a, bool) and 
              isinstance(b, (int, Integer)) and not isinstance(b, bool))
    except Exception:
        h2 = False

    # H_3: |a - b| < m
    try:
        h3 = bool(abs(a - b) < m)
    except Exception:
        h3 = False

    # ¬Q: a != b
    try:
        neg_q = bool(a != b)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: m is a positive integer",
    "H_2: a and b are integers",
    "H_3: |a - b| < m",
    "¬Q: a != b"
]

N_HYP = 3
NEG_Q_INDEX = 3