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

def conditions(witness) -> list[bool]:
    # H_1: G is a permutation group acting on a finite set
    try:
        h1 = isinstance(witness, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: G acts transitively on the set
    try:
        if callable(witness.is_transitive):
            h2 = bool(witness.is_transitive())
        else:
            h2 = bool(witness.is_transitive)
    except Exception:
        h2 = False

    # ¬Q: The order of the group G is exactly equal to the cardinality of the set (negated)
    try:
        if callable(witness.order):
            order = witness.order()
        else:
            order = witness.order
        degree = witness.degree
        neg_q = bool(order != degree)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a permutation group acting on a finite set",
    "H_2: G acts transitively on the set",
    "¬Q: The order of G is not equal to the cardinality of the set"
]

N_HYP = 2
NEG_Q_INDEX = 2