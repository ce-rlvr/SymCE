import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    # H_1: G is a group
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: The order of G is a finite integer n
    try:
        if h1:
            n = witness.order()
            h2 = int(n) > 0
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: G is not isomorphic to the additive group Z_n
    # Since G has order n, G is isomorphic to Z_n iff G is cyclic.
    # Therefore, the conclusion fails iff G is NOT cyclic.
    try:
        if h1 and h2:
            neg_q = not witness.is_cyclic
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: The order of G is a finite integer n",
    "¬Q: G is not isomorphic to Z_n (G is not cyclic)"
]

N_HYP = 2
NEG_Q_INDEX = 2