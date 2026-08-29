import sympy as sp
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if len(witness) != 4:
            return [False] * 5
        A, B, C, M = witness
        A = sp.Matrix(A)
        B = sp.Matrix(B)
        C = sp.Matrix(C)
        M = sp.Matrix(M)
    except Exception:
        return [False] * 5

    # H_1: A is an m x m diagonalizable matrix over a field F
    try:
        h1 = bool(A.is_square and A.is_diagonalizable())
    except Exception:
        h1 = False

    # H_2: B is an n x n diagonalizable matrix over a field F
    try:
        h2 = bool(B.is_square and B.is_diagonalizable())
    except Exception:
        h2 = False

    # H_3: C is an m x n matrix over F
    try:
        h3 = bool(C.rows == A.rows and C.cols == B.cols)
    except Exception:
        h3 = False

    # H_4: M is the block matrix A, C on top and 0, B on bottom
    try:
        m, n = A.rows, B.rows
        expected_M = sp.Matrix.vstack(sp.Matrix.hstack(A, C), sp.Matrix.hstack(sp.zeros(n, m), B))
        h4 = bool(M == expected_M)
    except Exception:
        h4 = False

    # neg_Q: M is not diagonalizable over F
    try:
        neg_q = not M.is_diagonalizable()
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: A is an m by m diagonalizable matrix over F",
    "H_2: B is an n by n diagonalizable matrix over F",
    "H_3: C is an m by n matrix over F",
    "H_4: M is the block matrix with A and C on top and 0 and B on bottom",
    "¬Q: M is not diagonalizable over F"
]

N_HYP = 4
NEG_Q_INDEX = 4