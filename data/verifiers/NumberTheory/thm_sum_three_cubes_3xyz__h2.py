import sympy
import math
import itertools
import functools

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False, False]
        x, y, z = witness
    except Exception:
        return [False, False]

    try:
        h1 = (isinstance(x, (int, sympy.Integer)) and 
              isinstance(y, (int, sympy.Integer)) and 
              isinstance(z, (int, sympy.Integer)))
    except Exception:
        h1 = False

    try:
        neg_q = not (x + y + z == 0 or (x == y and y == z))
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: x, y, z are integers",
    "¬Q: x + y + z != 0 and not (x == y == z)"
]

N_HYP = 1
NEG_Q_INDEX = 1