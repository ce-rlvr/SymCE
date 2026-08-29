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
        if callable(witness.order):
            order = witness.order()
        else:
            order = witness.order
        h1_ok = bool(order == 12)
    except Exception:
        h1_ok = False

    try:
        if callable(witness.is_solvable):
            solvable = witness.is_solvable()
        else:
            solvable = witness.is_solvable
        neg_q_ok = not bool(solvable)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: The order of G is 12",
    "¬Q: G is not a solvable group"
]

N_HYP = 1
NEG_Q_INDEX = 1