import sympy
from sympy import Matrix, eye, zeros

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 2:
            return [False, False, False]
        P1_raw, P2_raw = witness
    except Exception:
        return [False, False, False]

    # H_1: V_1 and V_2 are finite-dimensional vector spaces (P1 and P2 are square matrices)
    try:
        P1 = Matrix(P1_raw)
        P2 = Matrix(P2_raw)
        h1 = P1.is_square and P2.is_square
    except Exception:
        h1 = False

    # H_2: P_2 is a projection operator on V_2
    try:
        P2 = Matrix(P2_raw)
        h2 = P2.is_square and (P2**2 == P2)
    except Exception:
        h2 = False

    # ¬Q: P_1 \otimes P_2 is NOT a projection operator on V_1 \otimes V_2
    try:
        if h1:
            P1 = Matrix(P1_raw)
            P2 = Matrix(P2_raw)
            m, n = P1.shape
            p, q = P2.shape
            # Compute Kronecker product manually to avoid import path issues
            KP = Matrix(m * p, n * q, lambda i, j: P1[i // p, j // q] * P2[i % p, j % q])
            neg_q = (KP**2 != KP)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V_1 and V_2 are finite-dimensional vector spaces (P1 and P2 are square matrices)",
    "H_2: P_2 is a projection operator on V_2",
    "¬Q: P_1 \\otimes P_2 is NOT a projection operator on V_1 \\otimes V_2"
]

N_HYP = 2
NEG_Q_INDEX = 2