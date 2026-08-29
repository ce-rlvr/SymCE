import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup,
    AlternatingGroup,
    DihedralGroup,
    CyclicGroup
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
        h1_ok = isinstance(witness, PermutationGroup)
    except Exception:
        h1_ok = False

    try:
        h2_ok = h1_ok and (witness.order() % 2 == 0)
    except Exception:
        h2_ok = False

    try:
        # A finite group G has a normal subgroup of index 2 if and only if
        # its abelianization G/G' has even order.
        # Thus, G lacks a normal subgroup of index 2 iff the index of its
        # derived subgroup G' in G is odd.
        if not h1_ok:
            neg_q_ok = False
        else:
            derived_order = witness.derived_subgroup().order()
            index = witness.order() // derived_order
            neg_q_ok = (index % 2 != 0)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: The order of G is even",
    "¬Q: G does not possess a normal subgroup of index 2"
]

N_HYP = 2
NEG_Q_INDEX = 2