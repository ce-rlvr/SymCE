import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 2:
            return [False, False, False, False]
        A_raw, B_raw = witness
    except Exception:
        return [False, False, False, False]

    try:
        A = Matrix(A_raw)
        B = Matrix(B_raw)
        h1 = bool(A.is_square and B.is_square and A.shape == B.shape)
    except Exception:
        h1 = False

    try:
        h2 = bool(A.is_diagonalizable())
    except Exception:
        h2 = False

    try:
        h3 = bool(A * B == B * A)
    except Exception:
        h3 = False

    try:
        neg_q = not bool((A + B).is_diagonalizable())
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: A and B are n x n matrices",
    "H_2: A is diagonalizable",
    "H_3: A B = B A",
    "¬Q: A + B is not diagonalizable"
]

N_HYP = 3
NEG_Q_INDEX = 3