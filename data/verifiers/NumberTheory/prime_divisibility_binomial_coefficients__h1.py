import math
import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z

def conditions(witness):
    try:
        p, k = witness
    except Exception:
        return [False, False]

    try:
        h1 = isinstance(p, int) and isinstance(k, int) and 1 <= k <= p - 1
    except Exception:
        h1 = False

    try:
        neg_q = (math.comb(p, k) % p) != 0
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: k is an integer such that 1 <= k <= p-1",
    "¬Q: p does not divide binomial(p, k)"
]

N_HYP = 1
NEG_Q_INDEX = 1