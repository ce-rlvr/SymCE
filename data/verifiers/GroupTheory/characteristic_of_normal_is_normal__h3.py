import sympy
from sympy.combinatorics import Permutation, PermutationGroup
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
        G, N, K = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: N is a normal subgroup of G
    try:
        if isinstance(N, PermutationGroup):
            try:
                is_sub = N.is_subgroup(G)
                if is_sub:
                    h2 = bool(N.is_normal(G))
                else:
                    h2 = False
            except Exception:
                h2 = False
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: K is not a normal subgroup of G
    try:
        if isinstance(K, PermutationGroup):
            try:
                is_sub = K.is_subgroup(G)
                if is_sub:
                    is_norm = bool(K.is_normal(G))
                else:
                    is_norm = False
            except Exception:
                is_norm = False
            neg_q = not is_norm
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "¬Q: K is not a normal subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2