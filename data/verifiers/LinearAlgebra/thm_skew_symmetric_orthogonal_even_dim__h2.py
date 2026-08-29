import sympy
from sympy.matrices import MatrixBase, Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, MatrixBase):
            W = Matrix(witness)
        else:
            W = witness
    except Exception:
        W = None

    try:
        if W is not None and W.rows == W.cols:
            h1_ok = all(e.is_real for e in W)
        else:
            h1_ok = False
    except Exception:
        h1_ok = False

    try:
        if W is not None and W.rows == W.cols:
            h2_ok = bool(W == -W.T)
        else:
            h2_ok = False
    except Exception:
        h2_ok = False

    try:
        if W is not None and W.rows == W.cols:
            neg_q_ok = bool(W.rows % 2 != 0)
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: Q is an n x n real matrix",
    "H_2: Q is a skew-symmetric matrix",
    "¬Q: The dimension n is not an even integer"
]

N_HYP = 2
NEG_Q_INDEX = 2