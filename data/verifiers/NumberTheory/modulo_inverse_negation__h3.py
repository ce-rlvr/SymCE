import sympy
import math
import itertools
import functools

def conditions(witness):
    try:
        if isinstance(witness, dict):
            a = witness['a']
            x = witness['x']
            m = witness['m']
        else:
            a, x, m = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = isinstance(a, (int, sympy.Integer)) and \
             isinstance(x, (int, sympy.Integer)) and \
             isinstance(m, (int, sympy.Integer))
    except Exception:
        h1 = False

    try:
        h2 = m > 0
    except Exception:
        h2 = False

    try:
        neg_q = (((-a) * (-x)) % m) != (1 % m)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: a, x, m are integers",
    "H_2: m > 0",
    "¬Q: (-a)(-x) is not congruent to 1 mod m"
]

N_HYP = 2
NEG_Q_INDEX = 2