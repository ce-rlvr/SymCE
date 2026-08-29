import sympy
from sympy import Matrix, eye, zeros

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def kronecker(A, B):
    rA, cA = A.shape
    rB, cB = B.shape
    return Matrix(rA * rB, cA * cB, lambda i, j: A[i // rB, j // cB] * B[i % rB, j % cB])

def conditions(witness) -> list[bool]:
    try:
        A, B, C = witness
    except Exception:
        return [False, False, False, False, False]
    
    try:
        h1 = isinstance(A, sympy.MatrixBase) and isinstance(B, sympy.MatrixBase) and isinstance(C, sympy.MatrixBase)
    except Exception:
        h1 = False

    try:
        h2 = bool(B.is_square and B.is_diagonalizable())
    except Exception:
        h2 = False

    try:
        h3 = bool(A.is_square and C.rows == A.rows and C.cols == B.cols)
    except Exception:
        h3 = False

    try:
        n = A.rows
        m = B.rows
        K = kronecker(eye(m), A) - kronecker(B.T, eye(n))
        vecC = Matrix(n * m, 1, lambda k, _: C[k % n, k // n])
        h4 = bool(K.row_join(vecC).rank() == K.rank())
    except Exception:
        h4 = False

    try:
        n = A.rows
        m = B.rows
        M = Matrix.vstack(Matrix.hstack(A, C), Matrix.hstack(zeros(m, n), B))
        neg_q = not M.is_diagonalizable()
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: B is a diagonalizable m x m matrix over F",
    "H_3: C is an n x m matrix over F",
    "H_4: There exists an n x m matrix X over F such that AX - XB = C",
    "¬Q: The block upper triangular matrix is not diagonalizable over F"
]

N_HYP = 4
NEG_Q_INDEX = 4