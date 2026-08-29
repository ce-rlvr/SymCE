import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            B = witness.get('B')
            H = witness.get('H')
            K = witness.get('K')
        else:
            A, B, H, K = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = isinstance(A, PermutationGroup) and isinstance(B, PermutationGroup)
    except Exception:
        h1 = False

    try:
        h2 = isinstance(H, PermutationGroup) and H.is_subgroup(A)
    except Exception:
        h2 = False

    try:
        if not (isinstance(K, PermutationGroup) and K.is_subgroup(B)):
            neg_q = True
        else:
            neg_q = False
    except Exception:
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A and B are groups",
    "H_2: H is a subgroup of A with finite index",
    "¬Q: H x K is not a subgroup of A x B, or its index is not the product of their indices"
]

N_HYP = 2
NEG_Q_INDEX = 2