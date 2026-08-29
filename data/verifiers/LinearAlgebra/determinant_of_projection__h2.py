import sympy
from sympy import eye, zeros
from sympy.matrices.matrixbase import MatrixBase

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        h1 = isinstance(witness, MatrixBase) and witness.is_square and witness.shape[0] > 0
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            n = witness.shape[0]
            I = eye(n)
            is_identity = (witness == I)
            det_P = witness.det()
            
            if is_identity:
                q = (det_P == 1)
            else:
                q = (det_P == 0)
                
            neg_q = not q
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space of dimension n > 0 (witness is an n x n matrix)",
    "¬Q: The determinant of P is not (1 if P is the identity operator, and 0 otherwise)"
]

N_HYP = 1
NEG_Q_INDEX = 1