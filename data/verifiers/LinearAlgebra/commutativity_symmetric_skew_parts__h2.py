import sympy
from sympy import eye, zeros, Matrix
from sympy.matrices import MatrixBase

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H_1: Q is an n \times n real matrix
    try:
        if not isinstance(witness, MatrixBase):
            Q = Matrix(witness)
        else:
            Q = witness
            
        if Q.rows != Q.cols or Q.rows < 1:
            h1 = False
        else:
            h1 = all(e.is_real for e in Q)
    except Exception:
        h1 = False

    # neg_Q: Q + Q^T and Q - Q^T do NOT commute
    try:
        if not isinstance(witness, MatrixBase):
            Q = Matrix(witness)
        else:
            Q = witness
            
        S = Q + Q.T
        A = Q - Q.T
        diff = S * A - A * S
        neg_q = not all(sympy.simplify(e) == 0 for e in diff)
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: Q is an n x n real matrix",
    "¬Q: Q + Q^T and Q - Q^T do not commute"
]

N_HYP = 1
NEG_Q_INDEX = 1