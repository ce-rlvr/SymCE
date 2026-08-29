import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        h1 = isinstance(witness, Matrix) and witness.is_square
    except Exception:
        h1 = False

    try:
        if h1:
            h2 = bool((witness**2).is_diagonalizable())
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        if h1:
            neg_q = not bool(witness.is_diagonalizable())
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix over an algebraically closed field F of characteristic 0",
    "H_2: The matrix A^2 is diagonalizable over F",
    "¬Q: A is not diagonalizable over F"
]

N_HYP = 2
NEG_Q_INDEX = 2