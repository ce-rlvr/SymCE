import sympy
from sympy import I, eye, zeros, Matrix
from sympy.matrices import MatrixBase

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def _is_zero_mat(M):
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            if sympy.simplify(M[i, j]) != 0:
                return False
    return True

def conditions(witness):
    try:
        h1 = isinstance(witness, MatrixBase) and witness.is_square
    except Exception:
        h1 = False

    try:
        if not h1:
            h2 = False
        else:
            n = witness.shape[0]
            diff = witness * witness.H - eye(n)
            h2 = _is_zero_mat(diff)
    except Exception:
        h2 = False

    try:
        if not h1:
            neg_q = False
        else:
            n = witness.shape[0]
            diff2 = witness**2 - eye(n)
            neg_q = not _is_zero_mat(diff2)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: U is a square matrix",
    "H_2: U is a unitary matrix",
    "¬Q: U is not an involution (U^2 != I)"
]

N_HYP = 2
NEG_Q_INDEX = 2