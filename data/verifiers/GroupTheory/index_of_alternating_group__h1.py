import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
import math
import itertools
import functools

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
    try:
        h1 = isinstance(witness, int) and witness >= 1
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            sn_order = math.factorial(witness)
            an_order = math.factorial(witness) // 2 if witness > 1 else 1
            idx = sn_order // an_order
            neg_q = not (idx == 2)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "not Q: the index of An in Sn is not 2"
]

N_HYP = 1
NEG_Q_INDEX = 1