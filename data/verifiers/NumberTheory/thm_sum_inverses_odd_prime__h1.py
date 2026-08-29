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
        p = int(witness)
        if p <= 1:
            neg_q = False
        else:
            s = 0
            for i in range(1, p):
                s = (s + pow(i, -1, p)) % p
            neg_q = bool(s != 0)
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: sum of inverses modulo p is not 0"
]

N_HYP = 0
NEG_Q_INDEX = 0