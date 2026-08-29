import sympy
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
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
        G, N = witness
    except Exception:
        return [False, False]

    try:
        if isinstance(G, PermutationGroup):
            h1 = G.is_abelian
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        # A quotient group G/N is well-defined and is a group iff N is a normal subgroup of G.
        # If it is a valid group, we check if it is abelian.
        if not isinstance(G, PermutationGroup) or not isinstance(N, PermutationGroup):
            q_is_abelian = False
        elif not N.is_subgroup(G):
            q_is_abelian = False
        elif not N.is_normal(G):
            q_is_abelian = False
        else:
            Q = G.quotient_group(N)
            q_is_abelian = Q.is_abelian
    except Exception:
        q_is_abelian = False

    neg_q = not q_is_abelian

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is an abelian group",
    "¬Q: The quotient group G/N is not an abelian group"
]

N_HYP = 1
NEG_Q_INDEX = 1