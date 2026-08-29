import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_zero(M):
    if M.is_zero_matrix:
        return True
    for c in M:
        if sympy.simplify(c) != 0:
            return False
    return True

def conditions(witness):
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False]
        U, V = witness
        if not isinstance(U, sympy.MatrixBase) or not isinstance(V, sympy.MatrixBase):
            return [False, False]
        if U.shape != V.shape or U.rows != U.cols:
            return [False, False]
    except Exception:
        return [False, False]

    try:
        h1 = bool(is_zero(U * V - V * U))
    except Exception:
        h1 = False

    try:
        # A set of matrices can be simultaneously unitarily diagonalized 
        # if and only if they are all normal and they commute.
        is_U_normal = bool(is_zero(U * U.H - U.H * U))
        is_V_normal = bool(is_zero(V * V.H - V.H * V))
        commute = h1
        
        q = is_U_normal and is_V_normal and commute
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: U and V commute",
    "¬Q: U and V cannot be simultaneously unitarily diagonalized"
]

N_HYP = 1
NEG_Q_INDEX = 1