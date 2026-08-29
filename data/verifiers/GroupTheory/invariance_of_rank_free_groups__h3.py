import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
        if len(witness) == 4:
            F1, S1, F2, S2 = witness
        else:
            F1, F2 = witness
            S1 = F1.generators
            S2 = F2.generators
    except Exception:
        return [False, False, False]

    try:
        h1 = type(F1).__name__ == 'FreeGroup' and set(F1.generators) == set(S1)
    except Exception:
        h1 = False

    try:
        h2 = type(F2).__name__ == 'FreeGroup' and set(F2.generators) == set(S2)
    except Exception:
        h2 = False

    try:
        neg_q = len(set(S1)) != len(set(S2))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F1 is a free group on a set S1",
    "H_2: F2 is a free group on a set S2",
    "¬Q: The sets S1 and S2 do not have the same cardinality"
]

N_HYP = 2
NEG_Q_INDEX = 2