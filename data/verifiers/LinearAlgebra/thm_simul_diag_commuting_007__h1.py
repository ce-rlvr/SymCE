import sympy
from sympy import Matrix, eye, zeros

# Top-level setup: named object bindings that the witness expression may reference
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        P, Q = witness
        if not isinstance(P, Matrix):
            P = Matrix(P)
        if not isinstance(Q, Matrix):
            Q = Matrix(Q)
    except Exception:
        return [False, False]

    try:
        if P.shape != Q.shape or P.shape[0] != P.shape[1]:
            h1 = False
        else:
            h1 = bool(P * Q == Q * P)
    except Exception:
        h1 = False

    try:
        if P.shape != Q.shape or P.shape[0] != P.shape[1]:
            neg_q = False
        else:
            commute = bool(P * Q == Q * P)
            if not commute:
                # If they do not commute, they cannot be simultaneously diagonalizable
                neg_q = True
            else:
                # If they commute, they are simultaneously diagonalizable iff both are diagonalizable
                neg_q = not (P.is_diagonalizable() and Q.is_diagonalizable())
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: P and Q commute (PQ = QP)",
    "¬Q: P and Q are not simultaneously diagonalizable"
]

N_HYP = 1
NEG_Q_INDEX = 1