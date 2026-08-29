import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: A and B are n x n matrices
    try:
        A, B = witness
        h1 = (isinstance(A, Matrix) and isinstance(B, Matrix) and 
              A.shape == B.shape and A.shape[0] == A.shape[1])
    except Exception:
        h1 = False

    # H_2: A and B commute (AB = BA)
    try:
        A, B = witness
        h2 = bool(A * B == B * A)
    except Exception:
        h2 = False

    # ¬Q: A is not diagonalizable
    try:
        A, B = witness
        # is_diagonalizable() returns True if diagonalizable, False otherwise.
        # We want the negated conclusion, so we check if it is NOT diagonalizable.
        neg_q = not A.is_diagonalizable()
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A and B are n x n matrices",
    "H_2: A and B commute (AB = BA)",
    "¬Q: A is not diagonalizable"
]

N_HYP = 2
NEG_Q_INDEX = 2