import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)

# Top-level setup
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
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        A, B = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = isinstance(A, PermutationGroup) or hasattr(A, 'order')
    except Exception:
        h1 = False

    try:
        h2 = isinstance(B, PermutationGroup) or hasattr(B, 'order')
    except Exception:
        h2 = False

    try:
        a_non_trivial = A.order() > 1
        b_non_trivial = B.order() > 1
        neg_q = bool(a_non_trivial and b_non_trivial)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is a group",
    "H_2: B is a group",
    "¬Q: A * B is not an internal semidirect product of K and A x B"
]

N_HYP = 2
NEG_Q_INDEX = 2