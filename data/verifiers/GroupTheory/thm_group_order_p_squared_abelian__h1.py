import math
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

def conditions(witness) -> list[bool]:
    try:
        h1 = isinstance(witness, PermutationGroup) or hasattr(witness, 'is_group')
    except Exception:
        h1 = False

    try:
        order = witness.order()
        h2 = (math.isqrt(order) ** 2 == order)
    except Exception:
        h2 = False

    try:
        neg_q = not witness.is_abelian
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: The order of G is p^2",
    "¬Q: G is not an abelian group"
]

N_HYP = 2
NEG_Q_INDEX = 2