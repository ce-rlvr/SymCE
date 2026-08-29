import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, free_group
from sympy import oo

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

try:
    F1 = free_group("x")[0]
    F2 = free_group("x, y")[0]
    F3 = free_group("x, y, z")[0]
except Exception:
    pass

def conditions(witness) -> list[bool]:
    try:
        h1 = type(witness).__name__ == 'FreeGroup'
    except Exception:
        h1 = False

    try:
        if type(witness).__name__ == 'FreeGroup':
            # A free group is amenable if and only if its rank is 0 or 1
            neg_q = len(witness.generators) <= 1
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group",
    "¬Q: F is an amenable group"
]

N_HYP = 1
NEG_Q_INDEX = 1