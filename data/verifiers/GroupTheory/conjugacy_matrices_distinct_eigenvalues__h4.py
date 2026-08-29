import sympy as sp
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        A, B = witness
        if not isinstance(A, Matrix):
            A = Matrix(A)
        if not isinstance(B, Matrix):
            B = Matrix(B)
    except Exception:
        return [False, False, False, False]

    # H_1: A and B are square matrices of the same dimension n > 0
    try:
        h1 = bool((A.rows == A.cols) and (B.rows == B.cols) and (A.rows == B.rows) and (A.rows > 0))
    except Exception:
        h1 = False

    # H_2: A and B are in GL_n(F) (invertible)
    try:
        h2 = bool((A.det() != 0) and (B.det() != 0))
    except Exception:
        h2 = False

    # H_3: A and B have the exact same set of eigenvalues
    try:
        if A.charpoly() == B.charpoly():
            h3 = True
        else:
            evals_A = A.eigenvals()
            evals_B = B.eigenvals()
            h3 = bool((evals_A == evals_B) or (set(evals_A.keys()) == set(evals_B.keys())))
    except Exception:
        h3 = False

    # neg_Q: A and B are NOT conjugate in GL_n(F)
    try:
        if hasattr(A, 'is_similar'):
            are_sim = A.is_similar(B)
        else:
            if A.is_diagonalizable() != B.is_diagonalizable():
                are_sim = False
            else:
                are_sim = (A.jordan_form()[1] == B.jordan_form()[1])
        neg_q = not bool(are_sim)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: A and B are square matrices of the same dimension n > 0",
    "H_2: A and B are in GL_n(F) (invertible)",
    "H_3: A and B have the exact same set of eigenvalues",
    "¬Q: A and B are not conjugate in GL_n(F)"
]

N_HYP = 3
NEG_Q_INDEX = 3