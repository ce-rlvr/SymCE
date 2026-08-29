import sympy
from sympy.ntheory import divisors, totient
import math
import itertools
import functools

def conditions(witness):
    try:
        h1 = bool(isinstance(witness, (int, sympy.Integer)) and witness > 0)
    except Exception:
        h1 = False

    try:
        lhs = sum(totient(d) for d in divisors(witness))
        neg_q = bool(lhs != witness)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: sum_{d|n} phi(d) != n"
]

N_HYP = 1
NEG_Q_INDEX = 1