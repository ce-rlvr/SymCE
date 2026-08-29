import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        P, Q = witness
    except Exception:
        return [False, False]
    
    try:
        if not isinstance(P, Matrix):
            P = Matrix(P)
        if not isinstance(Q, Matrix):
            Q = Matrix(Q)
            
        if P.shape != Q.shape or P.shape[0] != P.shape[1]:
            h1 = False
        else:
            P_idempotent = all(sympy.simplify(a - b) == 0 for a, b in zip(P*P, P))
            P_hermitian = all(sympy.simplify(a - b) == 0 for a, b in zip(P, P.H))
            Q_idempotent = all(sympy.simplify(a - b) == 0 for a, b in zip(Q*Q, Q))
            Q_hermitian = all(sympy.simplify(a - b) == 0 for a, b in zip(Q, Q.H))
            h1 = P_idempotent and P_hermitian and Q_idempotent and Q_hermitian
    except Exception:
        h1 = False

    try:
        if not isinstance(P, Matrix):
            P = Matrix(P)
        if not isinstance(Q, Matrix):
            Q = Matrix(Q)
            
        QP = Q * P
        neg_q = not all(sympy.simplify(e) == 0 for e in QP)
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: P and Q are orthogonal projection matrices of the same dimensions",
    "¬Q: QP != 0"
]

N_HYP = 1
NEG_Q_INDEX = 1