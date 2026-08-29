import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.named_groups import *
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
from sympy.ntheory import *
from sympy.abc import *
from sympy.polys import *
import z3
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        h1 = True
        indices = witness.indices
        for i in indices:
            ring = witness.rings[i]
            subset = witness.subsets[i]
            if ring.one not in subset:
                h1 = False
                break
            for a in subset:
                for b in subset:
                    if ring.mul(a, b) not in subset:
                        h1 = False
                        break
            if not h1:
                break
                
        if h1:
            for i in indices:
                for j in indices:
                    if witness.leq(i, j):
                        for a in witness.subsets[i]:
                            if witness.phi(i, j, a) not in witness.subsets[j]:
                                h1 = False
                                break
    except Exception:
        h1 = False

    try:
        h2 = bool(witness.R_is_universal)
    except Exception:
        h2 = False

    try:
        h3 = bool(witness.S_is_universal)
    except Exception:
        h3 = False

    try:
        neg_q = not bool(witness.isomorphic_localizations)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: S_i <= R_i are multiplicative subsets such that phi_ij(S_i) <= S_j for all i <= j",
    "H_2: R is the direct limit of R_i",
    "H_3: S is the direct limit of S_i",
    "¬Q: The direct limit of the localized rings is not isomorphic to the localized ring S^{-1}R"
]

N_HYP = 3
NEG_Q_INDEX = 3