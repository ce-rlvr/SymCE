import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

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
        if len(witness) != 2:
            return [False, False, False, False]
        G, H = witness
    except Exception:
        return [False, False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: H is a subgroup of G
    try:
        h2 = False
        if isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup):
            h2 = all(g in G for g in H.generators)
    except Exception:
        h2 = False

    # H_3: H \subseteq Z(G)
    try:
        h3 = False
        if isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup):
            h3 = True
            for h in H.generators:
                for g in G.generators:
                    if h * g != g * h:
                        h3 = False
                        break
                if not h3:
                    break
    except Exception:
        h3 = False

    # ¬Q: H is not a normal subgroup of G
    try:
        neg_q = False
        if isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup):
            for h in H.generators:
                for g in G.generators:
                    if (g * h * g**-1) not in H:
                        neg_q = True
                        break
                if neg_q:
                    break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: H is a subgroup of G",
    "H_3: H is a subset of Z(G)",
    "¬Q: H is not a normal subgroup of G"
]

N_HYP = 3
NEG_Q_INDEX = 3