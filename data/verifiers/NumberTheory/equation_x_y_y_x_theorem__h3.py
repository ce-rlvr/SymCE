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

# Top-level setup
# (No specific named bindings required for this number theory conjecture)

def conditions(witness) -> list[bool]:
    try:
        # Witness is expected to be a tuple or list of two numbers: (x, y)
        x, y = witness
        # Check if x and y are positive integers
        h1 = (int(x) == x) and (int(y) == y) and (x > 0) and (y > 0)
    except Exception:
        h1 = False

    try:
        x, y = witness
        # Check if x < y
        h2 = bool(x < y)
    except Exception:
        h2 = False

    try:
        x, y = witness
        # The conclusion is that the only solution is x = 2 and y = 4.
        # The negated conclusion is that the witness is NOT (2, 4).
        neg_q = not (x == 2 and y == 4)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: x and y are positive integers",
    "H_2: x < y",
    "¬Q: x != 2 or y != 4"
]

N_HYP = 2
NEG_Q_INDEX = 2