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
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_isomorphic_to_D8(G):
    if G.order() != 8:
        return False
    if G.is_abelian:
        return False
    # D8 has exactly 2 elements of order 4 and 5 elements of order 2
    elements = list(G.generate())
    orders = [g.order() for g in elements]
    if orders.count(4) != 2:
        return False
    if orders.count(2) != 5:
        return False
    return True

def conditions(witness):
    # H_1: P is a subgroup of S4
    try:
        h1 = isinstance(witness, PermutationGroup) and witness.degree <= 4
    except Exception:
        h1 = False

    # ¬Q: P is not isomorphic to the dihedral group of order 8
    try:
        if not isinstance(witness, PermutationGroup):
            neg_q = False
        else:
            neg_q = not is_isomorphic_to_D8(witness)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: P is a subgroup of S4",
    "¬Q: P is not isomorphic to the dihedral group of order 8"
]

N_HYP = 1
NEG_Q_INDEX = 1