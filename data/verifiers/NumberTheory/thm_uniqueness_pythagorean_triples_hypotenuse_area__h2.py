import sympy
from sympy import Integer
import math
import itertools
import functools

def conditions(witness) -> list[bool]:
    try:
        t1, t2 = witness
        a1, b1, c1 = t1
        a2, b2, c2 = t2
    except Exception:
        return [False, False, False]

    try:
        h1 = (
            isinstance(a1, (int, Integer)) and isinstance(b1, (int, Integer)) and isinstance(c1, (int, Integer)) and
            isinstance(a2, (int, Integer)) and isinstance(b2, (int, Integer)) and isinstance(c2, (int, Integer)) and
            a1 > 0 and b1 > 0 and c1 > 0 and a2 > 0 and b2 > 0 and c2 > 0 and
            a1**2 + b1**2 == c1**2 and a2**2 + b2**2 == c2**2
        )
    except Exception:
        h1 = False

    try:
        h2 = (a1 * b1 == a2 * b2)
    except Exception:
        h2 = False

    try:
        neg_q = (set([a1, b1]) != set([a2, b2]))
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: (a_1, b_1, c_1) and (a_2, b_2, c_2) are Pythagorean triples",
    "H_2: The area of the right triangle with legs a_1 and b_1 equals the area of the right triangle with legs a_2 and b_2",
    "¬Q: The set of legs {a_1, b_1} is not identical to the set of legs {a_2, b_2}"
]

N_HYP = 2
NEG_Q_INDEX = 2