import sympy as sp
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

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
    def has_unique_QR(A):
        if not isinstance(A, sp.MatrixBase):
            try:
                A = sp.Matrix(A)
            except Exception:
                return False
        m, n = A.shape
        if m > n:
            return False
        A1 = A[:, :m]
        try:
            return A1.rank() == m
        except Exception:
            return False

    try:
        neg_q = not has_unique_QR(witness)
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: A does not have a unique QR factorization with strictly positive real diagonal entries"
]

N_HYP = 0
NEG_Q_INDEX = 0