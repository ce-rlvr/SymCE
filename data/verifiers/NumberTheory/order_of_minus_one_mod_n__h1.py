import sympy
import math
import itertools
import functools

def conditions(witness):
    try:
        if isinstance(witness, bool):
            return [False]
        if not isinstance(witness, (int, sympy.Integer)):
            return [False]
        n = int(witness)
        if n < 1:
            neg_q = False
        else:
            order = 1 if ((-1) % n == 1 % n) else 2
            neg_q = bool(order != 2)
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The multiplicative order of -1 modulo n is not exactly 2"
]

N_HYP = 0
NEG_Q_INDEX = 0