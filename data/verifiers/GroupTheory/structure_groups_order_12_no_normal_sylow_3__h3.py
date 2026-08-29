import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
import math
import itertools
import functools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    try:
        h2 = isinstance(witness, PermutationGroup) and witness.order() == 12
    except Exception:
        h2 = False

    try:
        if hasattr(witness, 'is_isomorphic'):
            neg_q = not witness.is_isomorphic(A4)
        else:
            neg_q = any(g.order() > 3 for g in witness.elements)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: The order of G is 12",
    "¬Q: G is not isomorphic to A_4"
]

N_HYP = 2
NEG_Q_INDEX = 2