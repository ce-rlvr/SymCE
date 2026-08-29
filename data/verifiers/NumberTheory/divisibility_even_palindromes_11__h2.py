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
        h2 = len(str(int(witness))) % 2 == 0
    except Exception:
        h2 = False

    try:
        neg_q = int(witness) % 11 != 0
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: the number of digits in the base-10 representation of n is even",
    "¬Q: n is not divisible by 11"
]

N_HYP = 2
NEG_Q_INDEX = 2