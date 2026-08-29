import sympy
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

def conditions(witness) -> list[bool]:
    try:
        L1 = witness.derived_subgroup()
        Z = witness.center()
        h1_ok = all(g in Z for g in L1.generators)
    except Exception:
        h1_ok = False

    try:
        L1 = witness.derived_subgroup()
        neg_q_ok = not L1.is_abelian
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: G is nilpotent of class at most 2",
    "¬Q: The commutator subgroup is not an abelian group"
]

N_HYP = 1
NEG_Q_INDEX = 1