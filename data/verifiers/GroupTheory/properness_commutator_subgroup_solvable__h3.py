import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

# Standard group theory objects
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
    # H_1: G is a group
    try:
        h1_ok = isinstance(witness, PermutationGroup)
    except Exception:
        h1_ok = False

    # H_2: G is not the trivial group
    try:
        h2_ok = h1_ok and witness.order() > 1
    except Exception:
        h2_ok = False

    # ¬Q: The commutator subgroup G' is NOT a proper subgroup of G (i.e. G' == G)
    try:
        neg_q_ok = h1_ok and witness.derived_subgroup().order() == witness.order()
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: G is not the trivial group",
    "¬Q: G' is not a proper subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2