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
        G, H, K = witness
    except Exception:
        return [False, False, False, False, False]

    # H_1: H is a subgroup of G
    try:
        h1 = H.is_subgroup(G)
    except Exception:
        h1 = False

    # H_2: K is a subgroup of G
    try:
        h2 = K.is_subgroup(G)
    except Exception:
        h2 = False

    # H_3: K contains H
    try:
        h3 = H.is_subgroup(K)
    except Exception:
        h3 = False

    # H_4: H is a normal subgroup of K
    try:
        h4 = H.is_normal(K)
    except Exception:
        h4 = False

    # ¬Q: K is not a subgroup of the normalizer N_G(H)
    try:
        is_sub = K.is_subgroup(G)
        k_in_normalizer = True
        for k in K.generators:
            for h in H.generators:
                if (k * h * ~k) not in H:
                    k_in_normalizer = False
                    break
            if not k_in_normalizer:
                break
        q = is_sub and k_in_normalizer
        neg_q = not q
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: K is a subgroup of G",
    "H_3: K contains H",
    "H_4: H is a normal subgroup of K",
    "¬Q: K is not a subgroup of the normalizer N_G(H)"
]

N_HYP = 4
NEG_Q_INDEX = 4