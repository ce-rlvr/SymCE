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
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        G, N, H = witness
    except Exception:
        return [False, False, False, False]

    # H_1: N is a normal subgroup of G
    try:
        h1 = False
        if N.is_subgroup(G):
            h1 = True
            for n in N.generators:
                for g in G.generators:
                    if (g * n * (g**-1)) not in N:
                        h1 = False
                        break
                if not h1:
                    break
    except Exception:
        h1 = False

    # H_2: N is a cyclic group
    try:
        h2 = False
        if hasattr(N, 'is_cyclic'):
            h2 = bool(N.is_cyclic)
        else:
            order = N.order()
            for n in N.elements:
                if n.order() == order:
                    h2 = True
                    break
    except Exception:
        h2 = False

    # H_3: H is a subgroup of N
    try:
        h3 = bool(H.is_subgroup(N))
    except Exception:
        h3 = False

    # ¬Q: H is not a normal subgroup of G
    try:
        is_H_normal_in_G = False
        if H.is_subgroup(G):
            is_H_normal_in_G = True
            for h in H.generators:
                for g in G.generators:
                    if (g * h * (g**-1)) not in H:
                        is_H_normal_in_G = False
                        break
                if not is_H_normal_in_G:
                    break
        neg_q = not is_H_normal_in_G
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: N is a cyclic group",
    "H_3: H is a subgroup of N",
    "¬Q: H is not a normal subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3