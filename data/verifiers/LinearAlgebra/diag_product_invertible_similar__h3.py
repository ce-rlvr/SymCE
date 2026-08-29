import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness satisfies the hypotheses and falsifies the conclusion.
    The witness should be a tuple of two square matrices (A, B).
    """
    try:
        A_input, B_input = witness
        A = Matrix(A_input)
        B = Matrix(B_input)
        h1 = (A.shape == B.shape) and (A.rows == A.cols) and (A.rows > 0)
    except Exception:
        h1 = False

    try:
        h2 = False
        if h1:
            h2 = (A.det() != 0)
    except Exception:
        h2 = False

    try:
        neg_q = False
        if h1:
            AB = A * B
            neg_q = not AB.is_diagonalizable()
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: A and B are n x n matrices",
    "H_2: A is an invertible matrix",
    "¬Q: AB is not diagonalizable"
]

N_HYP = 2
NEG_Q_INDEX = 2