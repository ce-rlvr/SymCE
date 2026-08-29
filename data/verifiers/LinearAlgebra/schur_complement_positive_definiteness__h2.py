import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_positive_definite(X):
    if not getattr(X, 'is_square', False):
        return False
    try:
        if not X.is_symmetric():
            return False
    except Exception:
        return False
        
    for i in range(1, X.rows + 1):
        try:
            d = X[:i, :i].det()
            if not (d > 0):
                return False
        except Exception:
            return False
    return True

def conditions(witness):
    """
    witness: tuple (A, B, C) of sympy Matrices representing the blocks of M
    """
    try:
        A, B, C = witness
        h1 = (getattr(A, 'is_square', False) and getattr(C, 'is_square', False) and
              A.rows > 0 and C.rows > 0 and
              A.rows == B.rows and C.rows == B.cols and
              A.is_symmetric() and C.is_symmetric())
    except Exception:
        h1 = False

    try:
        A, B, C = witness
        M = Matrix.vstack(Matrix.hstack(A, B), Matrix.hstack(B.T, C))
        M_pd = is_positive_definite(M)
        
        Schur = C - B.T * A.inv() * B
        Schur_pd = is_positive_definite(Schur)
        
        neg_q = (M_pd != Schur_pd)
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: M is a symmetric block matrix partitioned into blocks A, B, B_T, C",
    "¬Q: The equivalence M is positive definite iff Schur complement is positive definite fails"
]

N_HYP = 1
NEG_Q_INDEX = 1