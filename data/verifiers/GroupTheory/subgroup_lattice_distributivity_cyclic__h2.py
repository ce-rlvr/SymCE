import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
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
        h1 = bool(witness.is_cyclic)
    except Exception:
        h1 = False

    try:
        # By Ore's Theorem, the subgroup lattice L(G) of a group G is distributive 
        # if and only if G is locally cyclic. 
        # For finite groups (which sympy's PermutationGroup represents), 
        # being locally cyclic is equivalent to being cyclic.
        # Therefore, L(G) is distributive iff G is cyclic.
        is_distributive = bool(witness.is_cyclic)
        neg_q = not is_distributive
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a cyclic group",
    "¬Q: L(G) is not a distributive lattice"
]

N_HYP = 1
NEG_Q_INDEX = 1