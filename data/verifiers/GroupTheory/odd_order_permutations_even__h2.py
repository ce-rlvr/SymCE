import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    # H_1: Let n be a positive integer, Let \sigma be an element of S_n
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            n, sigma = witness
            h1 = isinstance(n, int) and n > 0 and isinstance(sigma, Permutation)
        else:
            sigma = witness
            h1 = isinstance(sigma, Permutation)
    except Exception:
        h1 = False

    # H_2: Assume the order of \sigma is an odd integer
    try:
        h2 = False
        if h1:
            h2 = (sigma.order() % 2 == 1)
    except Exception:
        h2 = False

    # ¬Q: \sigma is NOT an even permutation
    try:
        neg_q = False
        if h1:
            neg_q = not sigma.is_even
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: sigma is a permutation in S_n for some positive integer n",
    "H_2: the order of sigma is an odd integer",
    "¬Q: sigma is not an even permutation"
]

N_HYP = 2
NEG_Q_INDEX = 2