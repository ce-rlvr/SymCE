import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        P_raw, Q_raw = witness
        P = Matrix(P_raw)
        Q = Matrix(Q_raw)
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = bool(P.is_square and Q.is_square and P.shape == Q.shape)
    except Exception:
        h1 = False

    try:
        h2 = h1 and bool(P**2 == P) and bool(P.H == P)
    except Exception:
        h2 = False

    try:
        h3 = h1 and bool(Q**2 == Q) and bool(Q.H == Q)
    except Exception:
        h3 = False

    try:
        neg_q = h1 and bool(P * Q != Q * P)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: P and Q are square matrices of the same dimension",
    "H_2: P is an orthogonal projection matrix",
    "H_3: Q is an orthogonal projection matrix",
    "¬Q: P and Q do not commute"
]

N_HYP = 3
NEG_Q_INDEX = 3