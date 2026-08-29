import sympy
from sympy.ntheory import factorint, isprime
import itertools
import functools
import math

Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z10 = 10

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, int):
            rings = [witness]
        else:
            rings = list(witness)
        if not rings or not all(isinstance(r, int) and r >= 2 for r in rings):
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    try:
        h1 = True
    except Exception:
        h1 = False

    try:
        h2 = True
    except Exception:
        h2 = False

    try:
        h3 = True
        for r in rings:
            factors = factorint(r)
            if any(v > 1 for v in factors.values()):
                h3 = False
                break
    except Exception:
        h3 = False

    try:
        if len(rings) > 1:
            neg_q = True
        else:
            neg_q = not isprime(rings[0])
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R is an Artinian ring",
    "H_3: R is a reduced ring",
    "¬Q: R is not a field"
]

N_HYP = 3
NEG_Q_INDEX = 3