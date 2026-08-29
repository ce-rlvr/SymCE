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
        if isinstance(witness, dict):
            x = witness['x']
            y = witness['y']
        else:
            x, y = witness
    except Exception:
        return [False, False]

    try:
        h1 = (isinstance(x, (int, sympy.Integer)) and not isinstance(x, bool)) and \
             (isinstance(y, (int, sympy.Integer)) and not isinstance(y, bool))
    except Exception:
        h1 = False

    try:
        neg_q = not (x == 1 and y == 0)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x and y are integers",
    "¬Q: x != 1 or y != 0"
]

N_HYP = 1
NEG_Q_INDEX = 1