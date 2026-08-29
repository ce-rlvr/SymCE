import sympy
import math
import itertools
import functools

# No named bindings needed for number theory

def conditions(witness) -> list[bool]:
    try:
        a, b, c = witness
    except Exception:
        return [False, False]

    try:
        h1 = False
        if all(isinstance(x, (int, sympy.Integer)) for x in (a, b, c)):
            if all(x > 0 for x in (a, b, c)):
                h1 = True
    except Exception:
        h1 = False

    try:
        neg_q = bool(c == 2 * a)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a, b, and c are strictly positive integers",
    "¬Q: c == 2a"
]

N_HYP = 1
NEG_Q_INDEX = 1