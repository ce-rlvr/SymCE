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
        if len(witness) != 3:
            return [False, False, False]
        a, b, p = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = isinstance(a, (int, sympy.Integer)) and \
             isinstance(b, (int, sympy.Integer)) and \
             isinstance(p, (int, sympy.Integer)) and \
             p != 0
    except Exception:
        h1 = False

    try:
        h2 = (a * b) % p == 0
    except Exception:
        h2 = False

    try:
        neg_q = (a % p != 0) and (b % p != 0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a and b are integers",
    "H_2: ab == 0 (mod p)",
    "¬Q: a != 0 (mod p) and b != 0 (mod p)"
]

N_HYP = 2
NEG_Q_INDEX = 2