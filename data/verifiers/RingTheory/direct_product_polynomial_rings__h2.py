import sympy
from sympy import ZZ, QQ
import sympy.combinatorics
import sympy.matrices

S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
V4 = sympy.combinatorics.AlternatingGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R1, R2 = witness
        else:
            R1 = ZZ
            R2 = witness
    except Exception:
        return [False, False]

    try:
        h1 = bool(getattr(R1, 'is_commutative', False) and getattr(R1, 'is_ring', False))
    except Exception:
        h1 = False

    try:
        neg_q = not bool(getattr(R2, 'is_ring', False))
    except Exception:
        neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R_1 is a commutative ring",
    "not Q: The polynomial ring over R_1 x R_2 is not isomorphic to the product of polynomial rings"
]

N_HYP = 1
NEG_Q_INDEX = 1