import math
import itertools
import functools
import sympy
from sympy import abc

def conditions(witness) -> list[bool]:
    try:
        h1_ok = bool(isinstance(witness, int) and not isinstance(witness, bool) and witness >= 0)
    except Exception:
        h1_ok = False

    try:
        if isinstance(witness, int) and not isinstance(witness, bool) and witness >= 0:
            digit_sum = sum(int(d) for d in str(witness))
            neg_q = bool((witness % 9) != (digit_sum % 9))
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: n is a non-negative integer",
    "¬Q: n is not congruent to the sum of its digits modulo 9"
]

N_HYP = 1
NEG_Q_INDEX = 1