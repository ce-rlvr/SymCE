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
        G, N = witness
        h1 = hasattr(G, 'generators') and len(list(G.generators)) > 0
    except Exception:
        h1 = False

    try:
        G, N = witness
        if hasattr(N, 'is_subgroup') and hasattr(G, 'is_normal'):
            if not N.is_subgroup(G):
                neg_q = False
            else:
                # If N is not a normal subgroup, G/N is not a group,
                # hence it cannot be a finitely generated group.
                neg_q = not G.is_normal(N)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finitely generated group",
    "¬Q: The quotient group G/N is not finitely generated (or not a group)"
]

N_HYP = 1
NEG_Q_INDEX = 1