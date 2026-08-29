import sympy
from sympy.combinatorics import Permutation, PermutationGroup
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

def conditions(witness):
    try:
        G, G_prime = witness
    except Exception:
        return [False, False]

    try:
        K = G.derived_subgroup()
        h1 = bool(G_prime.is_subgroup(K) and K.is_subgroup(G_prime))
    except Exception:
        h1 = False

    try:
        neg_q = not bool(G_prime.is_normal(G))
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G' is the commutator subgroup of G",
    "¬Q: G' is not a normal subgroup of G"
]

N_HYP = 1
NEG_Q_INDEX = 1