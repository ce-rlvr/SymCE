import sympy
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
A5 = AlternatingGroup(5)
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
        h1 = bool(witness.order() > 1)
    except Exception:
        h1 = False

    try:
        derived = witness.derived_subgroup()
        neg_q = bool(derived.order() == witness.order())
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = ["H_1: G is not the trivial group", "¬Q: G/G' is the trivial group"]

N_HYP = 1
NEG_Q_INDEX = 1