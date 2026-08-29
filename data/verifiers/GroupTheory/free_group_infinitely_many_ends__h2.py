import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import free_group
from sympy.matrices import eye, zeros

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

try:
    F1 = free_group("x")[0]
    F2 = free_group("x, y")[0]
except Exception:
    pass

def conditions(witness) -> list[bool]:
    try:
        is_free = type(witness).__name__ == 'FreeGroup'
        is_fp_free = type(witness).__name__ == 'FpGroup' and len(witness.relators) == 0
        h1 = bool(is_free or is_fp_free)
    except Exception:
        h1 = False

    try:
        if type(witness).__name__ == 'FreeGroup':
            neg_q = bool(len(witness.generators) < 2)
        elif type(witness).__name__ == 'FpGroup' and len(witness.relators) == 0:
            neg_q = bool(len(witness.generators) < 2)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a finitely generated free group",
    "¬Q: F does not have infinitely many ends"
]

N_HYP = 1
NEG_Q_INDEX = 1