import sympy
import math
import itertools
import functools

# Top-level setup
# (No named bindings needed for this number theory conjecture)

def conditions(witness) -> list[bool]:
    try:
        a, b, k, m = witness
    except Exception:
        return [False, False, False, False]

    try:
        h1 = isinstance(a, int) and isinstance(b, int)
    except Exception:
        h1 = False

    try:
        h2 = isinstance(k, int)
    except Exception:
        h2 = False

    try:
        h3 = (a - b) % m == 0
    except Exception:
        h3 = False

    try:
        neg_q = (a + k * m - b) % m != 0
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: a and b are integers",
    "H_2: k is an integer",
    "H_3: a == b (mod m)",
    "¬Q: a + km != b (mod m)"
]

N_HYP = 3
NEG_Q_INDEX = 3