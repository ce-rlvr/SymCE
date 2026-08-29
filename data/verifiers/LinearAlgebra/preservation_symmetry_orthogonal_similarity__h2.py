import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False]
        A_raw, Q_raw = witness
        A = Matrix(A_raw)
        Q = Matrix(Q_raw)
    except Exception:
        return [False, False]
        
    try:
        if not (A.is_square and Q.is_square and A.shape == Q.shape):
            h1 = False
        elif not all(x.is_real for x in A) or not all(x.is_real for x in Q):
            h1 = False
        elif Q.det() == 0:
            h1 = False
        else:
            diffA = sympy.simplify(A - A.T)
            h1 = all(x == 0 for x in diffA)
    except Exception:
        h1 = False
        
    try:
        M = Q * A * Q.inv()
        diffM = sympy.simplify(M - M.T)
        neg_q = not all(x == 0 for x in diffM)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: A is an n x n real symmetric matrix and Q is an n x n real invertible matrix",
    "¬Q: Q A Q^{-1} is not a symmetric matrix"
]

N_HYP = 1
NEG_Q_INDEX = 1