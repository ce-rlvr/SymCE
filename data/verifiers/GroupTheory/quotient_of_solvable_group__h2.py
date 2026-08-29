import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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
        G, N = witness
    except Exception:
        return [False, False]

    try:
        h1 = bool(G.is_solvable)
    except Exception:
        h1 = False

    try:
        if not isinstance(N, PermutationGroup):
            neg_q = True
        elif not N.is_subgroup(G):
            neg_q = True
        elif not G.is_normal(N):
            neg_q = True
        else:
            Q_group = G.quotient_group(N)
            neg_q = not bool(Q_group.is_solvable)
    except Exception:
        neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a solvable group",
    "¬Q: G/N is not a solvable group"
]

N_HYP = 1
NEG_Q_INDEX = 1