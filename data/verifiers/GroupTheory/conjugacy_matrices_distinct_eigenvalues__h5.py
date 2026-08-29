import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        A, B = witness
        A = sympy.Matrix(A)
        B = sympy.Matrix(B)
    except Exception:
        return [False, False, False, False]
    
    try:
        h1 = A.is_square and B.is_square and A.shape == B.shape and A.shape[0] > 0
    except Exception:
        h1 = False

    try:
        h2 = h1 and (A.det() != 0) and (B.det() != 0)
    except Exception:
        h2 = False

    try:
        if h1:
            n = A.shape[0]
            evals_A = A.eigenvals()
            evals_B = B.eigenvals()
            h3 = (len(evals_A) == n) and (len(evals_B) == n)
        else:
            h3 = False
    except Exception:
        h3 = False

    try:
        if h1:
            try:
                neg_q = not A.is_similar(B)
            except Exception:
                neg_q = A.charpoly() != B.charpoly()
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: A and B are square matrices of the same dimension n > 0",
    "H_2: A and B are in GL_n(F) (invertible)",
    "H_3: A and B each have n distinct eigenvalues",
    "¬Q: A and B are not conjugate"
]

N_HYP = 3
NEG_Q_INDEX = 3