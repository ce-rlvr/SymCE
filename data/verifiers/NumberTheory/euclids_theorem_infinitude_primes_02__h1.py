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

def conditions(witness):
    try:
        if bool(2 > witness):
            c = True
        else:
            p = sympy.nextprime(witness)
            c = sympy.isprime(p) and bool(p > witness)
    except Exception:
        c = False

    neg_q = not c
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: There does not exist a prime number p such that p > n"
]

N_HYP = 0
NEG_Q_INDEX = 0