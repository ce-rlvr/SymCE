import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness):
    neg_q = False
    try:
        if hasattr(witness, 'is_commutative'):
            if witness.is_commutative is False:
                neg_q = True
        elif hasattr(witness, 'is_Matrix') and witness.is_Matrix:
            neg_q = True
        elif isinstance(witness, str):
            if any(w in witness.lower() for w in ['noncommutative', 'quaternion', 'matrix', 'free algebra', 'weyl']):
                neg_q = True
    except Exception:
        pass
    return [bool(neg_q)]

CONDITION_LABELS = [
    "¬Q: R is not commutative"
]

N_HYP = 0
NEG_Q_INDEX = 0