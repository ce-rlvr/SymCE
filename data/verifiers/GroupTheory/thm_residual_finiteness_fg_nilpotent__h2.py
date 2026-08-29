import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        if hasattr(witness, 'is_nilpotent'):
            val = witness.is_nilpotent
            h1 = val() if callable(val) else bool(val)
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        if hasattr(witness, 'is_residually_finite'):
            val = witness.is_residually_finite
            res_fin = val() if callable(val) else bool(val)
        elif hasattr(witness, 'is_finite') and witness.is_finite:
            res_fin = True
        else:
            res_fin = True
        neg_q = not res_fin
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a nilpotent group",
    "¬Q: G is not residually finite"
]

N_HYP = 1
NEG_Q_INDEX = 1