import sympy
import math
import itertools
import functools

def conditions(witness) -> list[bool]:
    try:
        a, b, n = witness
    except Exception:
        return [False, False, False]

    try:
        h1_ok = bool(isinstance(a, int) and isinstance(b, int) and a > 0 and b > 0)
    except Exception:
        h1_ok = False

    try:
        h2_ok = bool(isinstance(n, int) and n > 0)
    except Exception:
        h2_ok = False

    try:
        neg_q_ok = bool(b % a != 0)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: a and b are positive integers",
    "H_2: n is a positive integer",
    "¬Q: a does not divide b"
]

N_HYP = 2
NEG_Q_INDEX = 2