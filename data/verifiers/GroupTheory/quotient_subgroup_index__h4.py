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
        G, N, H = witness
    except Exception:
        return [False, False, False, False, False]

    def get_order(grp):
        return grp.order() if callable(grp.order) else grp.order

    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    try:
        h2 = isinstance(N, PermutationGroup) and N.is_subgroup(G) and G.is_normal(N)
    except Exception:
        h2 = False

    try:
        h3 = isinstance(H, PermutationGroup) and H.is_subgroup(G)
    except Exception:
        h3 = False

    try:
        h4 = h3 and (get_order(G) % get_order(H) == 0)
    except Exception:
        h4 = False

    try:
        if not (h1 and h2 and h3):
            neg_q = False
        elif not N.is_subgroup(H):
            # If N is not a subgroup of H, H/N is not a valid quotient subgroup.
            # The conclusion assumes H/N is a quotient subgroup, so it fails.
            neg_q = True
        else:
            order_G = get_order(G)
            order_N = get_order(N)
            order_H = get_order(H)
            
            index_HN_GN_exact = (order_G // order_N) // (order_H // order_N)
            index_G_H_exact = order_G // order_H
            
            neg_q = index_HN_GN_exact != index_G_H_exact
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "H_3: H is a subgroup of G",
    "H_4: The index of H in G is finite",
    "not Q: The index of H/N in G/N is not equal to the index of H in G"
]

N_HYP = 4
NEG_Q_INDEX = 4