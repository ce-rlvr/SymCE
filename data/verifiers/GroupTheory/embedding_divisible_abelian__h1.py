import sympy
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
        # A group embeds into an abelian group if and only if it is abelian.
        # Thus, it embeds into a divisible abelian group iff it is abelian.
        # The conclusion fails (neg_Q is True) iff the group is non-abelian.
        neg_q = bool(not witness.is_abelian)
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: G does not embed into a divisible abelian group (G is non-abelian)"
]

N_HYP = 0
NEG_Q_INDEX = 0