import sympy
from sympy.combinatorics import PermutationGroup
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
        if callable(witness.is_nilpotent):
            h1 = bool(witness.is_nilpotent())
        else:
            h1 = bool(witness.is_nilpotent)
    except Exception:
        h1 = False

    try:
        if callable(witness.center):
            center = witness.center()
        else:
            center = witness.center
            
        if callable(center.order):
            c_order = center.order()
        else:
            c_order = center.order
            
        neg_q = bool(c_order == 1)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a nilpotent group",
    "¬Q: The center Z(G) is the trivial group"
]

N_HYP = 1
NEG_Q_INDEX = 1