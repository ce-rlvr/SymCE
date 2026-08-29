import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        P, Q = witness
        h1 = bool(isinstance(P, sympy.MatrixBase) and isinstance(Q, sympy.MatrixBase) and 
                  P.is_square and Q.is_square and P.shape == Q.shape)
    except Exception:
        h1 = False

    try:
        P, Q = witness
        C = P * Q - Q * P
        neg_q = bool(C.rank() % 2 != 0)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: P and Q are square matrices of the same size",
    "¬Q: The rank of C = PQ - QP is not an even integer"
]

N_HYP = 1
NEG_Q_INDEX = 1