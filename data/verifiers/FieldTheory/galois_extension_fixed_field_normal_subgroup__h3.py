import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False]
        G, H = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        h2 = isinstance(H, PermutationGroup) and H.is_subgroup(G) and H.is_normal(G)
    except Exception:
        h2 = False

    try:
        if not (isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup) and H.is_subgroup(G)):
            neg_q = False
        else:
            is_galois = H.is_normal(G)
            degree_eq = True
            q = is_galois and degree_eq
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: L over K is a finite Galois extension with Galois group G",
    "H_2: H is a normal subgroup of G",
    "not Q: L_H over K is not a Galois extension or its degree is not equal to the index of H in G"
]

N_HYP = 2
NEG_Q_INDEX = 2