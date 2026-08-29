import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup,
    AlternatingGroup,
    DihedralGroup,
    CyclicGroup,
    AbelianGroup
)

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        A, B, C = witness
    except Exception:
        return [False, False, False, False]

    try:
        h1_ok = bool(isinstance(A, PermutationGroup) and A.is_abelian)
    except Exception:
        h1_ok = False

    try:
        h2_ok = bool(isinstance(B, PermutationGroup) and B.is_abelian)
    except Exception:
        h2_ok = False

    try:
        h3_ok = bool(isinstance(C, PermutationGroup) and C.is_abelian)
    except Exception:
        h3_ok = False

    try:
        neg_q_ok = not bool(B.is_isomorphic(C))
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: A is a finite abelian group",
    "H_2: B is a finite abelian group",
    "H_3: C is a finite abelian group",
    "¬Q: B is not isomorphic to C"
]

N_HYP = 3
NEG_Q_INDEX = 3