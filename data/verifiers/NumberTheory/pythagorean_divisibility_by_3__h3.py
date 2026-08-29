import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

def conditions(witness) -> list[bool]:
    try:
        a, b, c = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = False
        if all(isinstance(x, (int, sympy.Integer)) for x in (a, b, c)):
            if a > 0 and b > 0 and c > 0:
                h1 = True
    except Exception:
        h1 = False

    try:
        h2 = bool(a**2 + b**2 == c**2)
    except Exception:
        h2 = False

    try:
        div_a = (a % 3 == 0)
        div_b = (b % 3 == 0)
        exactly_one = (div_a != div_b)
        neg_q = not exactly_one
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a, b, and c are positive integers",
    "H_2: a^2 + b^2 = c^2",
    "¬Q: It is not the case that exactly one of a or b is divisible by 3"
]

N_HYP = 2
NEG_Q_INDEX = 2