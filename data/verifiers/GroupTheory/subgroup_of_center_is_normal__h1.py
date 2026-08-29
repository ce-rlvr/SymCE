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

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 2:
            return [False, False, False, False]
        G, H = witness
    except Exception:
        return [False, False, False, False]

    # H_1: Z(G) is the center of G (G is a group)
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: H is a subgroup of G
    try:
        if isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup):
            h2 = bool(H.is_subgroup(G))
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: H \subseteq Z(G)
    try:
        if isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup):
            Z = G.center()
            h3 = all(g in Z for g in H.generators)
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: H is not a normal subgroup of G
    try:
        if isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup):
            neg_q = not bool(H.is_normal(G))
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: Z(G) is the center of G",
    "H_2: H is a subgroup of G",
    "H_3: H is a subset of Z(G)",
    "¬Q: H is not a normal subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3