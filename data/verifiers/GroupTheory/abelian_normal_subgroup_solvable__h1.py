import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

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
        h1 = bool(witness.is_solvable)
    except Exception:
        h1 = False

    try:
        h2 = bool(witness.order() > 1)
    except Exception:
        h2 = False

    try:
        has_non_trivial_abelian_normal = False
        for H in witness.normal_subgroups():
            if H.is_abelian and H.order() > 1:
                has_non_trivial_abelian_normal = True
                break
        neg_q = not has_non_trivial_abelian_normal
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is solvable",
    "H_2: G is not the trivial group",
    "¬Q: G does not contain a non-trivial abelian normal subgroup"
]

N_HYP = 2
NEG_Q_INDEX = 2