import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics import free_group
from sympy.matrices import eye, zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

F1 = free_group("x")[0]
F2 = free_group("x, y")[0]
F3 = free_group("x, y, z")[0]
F4 = free_group("x, y, z, w")[0]

FreeGroupType = type(F1)

def conditions(witness):
    try:
        h1 = isinstance(witness, FreeGroupType)
    except Exception:
        h1 = False

    try:
        if h1:
            # Out(F_n) is isomorphic to GL(2, Z) if and only if n = 2.
            # Therefore, it is NOT isomorphic when the rank is not 2.
            neg_q = len(witness.generators) != 2
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group",
    "¬Q: Out(F) is not isomorphic to GL(2, Z)"
]

N_HYP = 1
NEG_Q_INDEX = 1