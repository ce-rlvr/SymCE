import sympy as sp
from sympy import Matrix, eye, zeros
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    A = None
    T = None
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            T = witness.get('T')
        elif hasattr(witness, 'A') and hasattr(witness, 'T'):
            A = witness.A
            T = witness.T
        elif isinstance(witness, tuple):
            A = witness[0]
            if len(witness) == 2:
                T = witness[1]
            elif len(witness) >= 3:
                T = witness[2]
        elif isinstance(witness, sp.MatrixBase):
            A = witness
            T = A.upper_triangular()
    except Exception:
        pass

    # H_1: A is an n x n matrix over the complex numbers
    try:
        h1 = isinstance(A, sp.MatrixBase) and A.is_square
    except Exception:
        h1 = False

    # H_2: The upper triangular matrix T is a diagonal matrix
    try:
        h2 = isinstance(T, sp.MatrixBase) and T.is_diagonal()
    except Exception:
        h2 = False

    # ¬Q: The matrix A is not unitarily diagonalizable
    # A complex square matrix is unitarily diagonalizable iff it is normal (A * A^H = A^H * A)
    try:
        if not (isinstance(A, sp.MatrixBase) and A.is_square):
            neg_q = False
        else:
            diff = A * A.H - A.H * A
            is_normal = True
            for i in range(diff.rows):
                for j in range(diff.cols):
                    if sp.simplify(diff[i, j]) != 0:
                        is_normal = False
                        break
                if not is_normal:
                    break
            neg_q = not is_normal
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix over the complex numbers",
    "H_2: The upper triangular matrix T is a diagonal matrix",
    "¬Q: The matrix A is not unitarily diagonalizable"
]

N_HYP = 2
NEG_Q_INDEX = 2