import sympy
import math
import itertools
import functools

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 2:
            return [False, False]
        x, y = witness
        if not isinstance(x, (int, sympy.Integer)) or not isinstance(y, (int, sympy.Integer)):
            return [False, False]
    except Exception:
        return [False, False]

    try:
        h1 = bool(x**2 - 2 * y**4 == -1)
    except Exception:
        h1 = False

    try:
        q = ((x == 1 and y == 1) or (x == 239 and y == 13))
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x^2 - 2y^4 = -1",
    "¬Q: not ((x = 1 and y = 1) or (x = 239 and y = 13))"
]

N_HYP = 1
NEG_Q_INDEX = 1