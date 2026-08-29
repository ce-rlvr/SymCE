import sympy
from sympy.matrices import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: A is a square matrix
    try:
        h1 = witness.is_square
    except Exception:
        h1 = False

    # H_2: A is diagonalizable
    try:
        h2 = witness.is_diagonalizable()
    except Exception:
        h2 = False

    # ¬Q: A is not the zero matrix
    try:
        neg_q = not witness.is_zero_matrix
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: A is a square matrix",
    "H_2: A is diagonalizable",
    "¬Q: A is not the zero matrix"
]

N_HYP = 2
NEG_Q_INDEX = 2