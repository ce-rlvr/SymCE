import sympy
import math
import itertools
import functools
from sympy.abc import x, y, z

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            S = witness.get('S')
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            n, S = witness
        else:
            n, S = None, None
    except Exception:
        return [False, False]

    try:
        h1_ok = isinstance(n, int) and n > 0
    except Exception:
        h1_ok = False

    try:
        if isinstance(n, int) and isinstance(S, int):
            neg_q_ok = (n % 3) != (S % 3)
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: n is not congruent to S mod 3"
]

N_HYP = 1
NEG_Q_INDEX = 1