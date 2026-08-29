import sympy as sp
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            A = witness['A']
            u = witness['u']
            v = witness['v']
        elif isinstance(witness, (tuple, list)) and len(witness) == 3:
            A, u, v = witness
        else:
            return [False, False, False]
            
        if not isinstance(A, sp.MatrixBase):
            A = sp.Matrix(A)
        if not isinstance(u, sp.MatrixBase):
            u = sp.Matrix(u)
        if not isinstance(v, sp.MatrixBase):
            v = sp.Matrix(v)
    except Exception:
        return [False, False, False]

    try:
        h1 = bool(A.is_square and u.shape == (A.rows, 1) and v.shape == (A.rows, 1))
    except Exception:
        h1 = False

    try:
        dot = v.dot(u)
        h2 = bool(sp.simplify(dot) != 0)
    except Exception:
        h2 = False

    try:
        neg_q = not A.is_diagonalizable()
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix, u and v are n x 1 vectors",
    "H_2: The dot product v^T u is non-zero",
    "¬Q: The matrix A is not diagonalizable"
]

N_HYP = 2
NEG_Q_INDEX = 2