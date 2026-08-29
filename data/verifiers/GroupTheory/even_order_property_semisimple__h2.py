import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup,
    AlternatingGroup,
    DihedralGroup,
    CyclicGroup
)

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z5 = CyclicGroup(5)
Z6 = CyclicGroup(6)
Z7 = CyclicGroup(7)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    # H_1: G is a finite group
    try:
        h1 = isinstance(witness, PermutationGroup) and witness.order() > 0
    except Exception:
        h1 = False

    # H_2: G is a non-trivial group
    try:
        h2 = isinstance(witness, PermutationGroup) and witness.order() > 1
    except Exception:
        h2 = False

    # ¬Q: The order of G is not an even integer
    try:
        neg_q = isinstance(witness, PermutationGroup) and witness.order() % 2 != 0
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is a non-trivial group",
    "¬Q: The order of G is not an even integer"
]

N_HYP = 2
NEG_Q_INDEX = 2