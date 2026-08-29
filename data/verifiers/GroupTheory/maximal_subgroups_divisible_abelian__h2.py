import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

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

def conditions(witness) -> list[bool]:
    # H_1: G is an abelian group
    try:
        h1_ok = bool(witness.is_abelian)
    except Exception:
        h1_ok = False

    # ¬Q: G has a maximal subgroup
    try:
        # For finite groups, a maximal subgroup exists if and only if the group is non-trivial.
        # Since SymPy's PermutationGroup only represents finite groups, we can check order > 1.
        neg_q_ok = bool(witness.order() > 1)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is an abelian group",
    "¬Q: G has a maximal subgroup"
]

N_HYP = 1
NEG_Q_INDEX = 1