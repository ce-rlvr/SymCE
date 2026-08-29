import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 2:
            return [False, False, False]
        A, B = witness
    except Exception:
        return [False, False, False]

    # H_1: A and B are n x n matrices
    try:
        h1 = bool(hasattr(A, 'is_square') and hasattr(B, 'is_square') and 
                  A.is_square and B.is_square and A.shape == B.shape)
    except Exception:
        h1 = False

    # H_2: B commutes with A (AB = BA)
    try:
        h2 = bool(A * B == B * A)
    except Exception:
        h2 = False

    # ¬Q: B is not diagonalizable
    try:
        neg_q = (B.is_diagonalizable() is False)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A and B are n x n matrices",
    "H_2: B commutes with A (AB = BA)",
    "¬Q: B is not diagonalizable"
]

N_HYP = 2
NEG_Q_INDEX = 2