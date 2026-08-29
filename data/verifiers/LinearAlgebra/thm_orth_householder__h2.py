from sympy import eye, zeros
from sympy.matrices import MatrixBase

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        v, H = witness
        h1_ok = False
        if isinstance(v, MatrixBase) and isinstance(H, MatrixBase):
            if not v.is_zero and (v.rows == 1 or v.cols == 1):
                n = max(v.rows, v.cols)
                if H.rows == n and H.cols == n:
                    h1_ok = True
    except Exception:
        h1_ok = False

    try:
        v, H = witness
        neg_q_ok = False
        if isinstance(H, MatrixBase):
            n = H.rows
            if H.T * H != eye(n):
                neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: v is a non-zero vector in R^n and H is an n x n matrix",
    "¬Q: H is not an orthogonal matrix"
]

N_HYP = 1
NEG_Q_INDEX = 1