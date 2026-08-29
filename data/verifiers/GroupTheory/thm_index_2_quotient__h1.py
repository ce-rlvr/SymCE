import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
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
V4 = DihedralGroup(2)
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
        G, H = witness
    except Exception:
        return [False, False, False]
    
    # H_1: H is a subgroup of G
    try:
        h1 = bool(H.is_subgroup(G))
    except Exception:
        h1 = False
        
    # H_2: index of H in G is 2
    try:
        h2 = bool(G.order() == 2 * H.order())
    except Exception:
        h2 = False
        
    # not Q: H is not a normal subgroup of G or G/H is not isomorphic to Z_2
    try:
        is_normal = bool(H.is_normal(G))
        index_2 = bool(G.order() == 2 * H.order())
        q = is_normal and index_2
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: index of H in G is 2",
    "not Q: H is not a normal subgroup of G or G/H is not isomorphic to Z_2"
]

N_HYP = 2
NEG_Q_INDEX = 2