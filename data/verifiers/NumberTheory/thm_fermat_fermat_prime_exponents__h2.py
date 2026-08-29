import sympy
import math
import itertools
import functools

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, (int, sympy.Integer)):
            n = int(witness)
            h1 = (n > 0)
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        if isinstance(witness, (int, sympy.Integer)):
            n = int(witness)
            is_power_of_2 = (n > 0) and ((n & (n - 1)) == 0)
            neg_q = not is_power_of_2
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: n is not a power of 2"
]

N_HYP = 1
NEG_Q_INDEX = 1