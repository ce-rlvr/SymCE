import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    try:
        h1 = bool(witness.is_nilpotent)
    except Exception:
        h1 = False

    try:
        is_abelian = bool(witness.is_abelian)
        derived = witness.derived_subgroup()
        center = witness.center()
        derived_in_center = bool(derived.is_subgroup(center))
        
        # The conclusion is that G/Z(G) is a non-trivial abelian group.
        # G/Z(G) is trivial iff G is abelian.
        # G/Z(G) is abelian iff [G,G] <= Z(G).
        # Therefore, the conclusion holds iff G is not abelian AND [G,G] <= Z(G).
        conclusion = (not is_abelian) and derived_in_center
        neg_q = not conclusion
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a nilpotent group",
    "¬Q: G/Z(G) is trivial or not abelian"
]

N_HYP = 1
NEG_Q_INDEX = 1