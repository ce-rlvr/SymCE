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

def conditions(witness):
    try:
        # The conclusion is that the derived series is constant, i.e., G^(n) == G for all n >= 0.
        # This holds if and only if G^(1) == G (G is a perfect group).
        # The negation is that G^(1) != G.
        # Since G^(1) is always a subgroup of G, they are equal iff their orders are equal.
        neg_q = witness.derived_subgroup().order() != witness.order()
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The derived series of G is not constant (G is not perfect)"
]

N_HYP = 0
NEG_Q_INDEX = 0