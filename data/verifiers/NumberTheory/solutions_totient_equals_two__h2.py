import sympy
import math
import itertools
import functools

def conditions(witness) -> list[bool]:
    try:
        h1 = (type(witness) is int or isinstance(witness, sympy.Integer)) and witness > 0
    except Exception:
        h1 = False

    try:
        neg_q = witness not in {3, 4, 6}
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x is a positive integer",
    "¬Q: x is not in {3, 4, 6}"
]

N_HYP = 1
NEG_Q_INDEX = 1