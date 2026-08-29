import sympy
from sympy import Matrix, MatrixBase, eye, zeros, sqrt, simplify, expand

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_zero_mat(M):
    if M.is_zero_matrix:
        return True
    M_exp = expand(M)
    if M_exp.is_zero_matrix:
        return True
    for i in range(M.rows):
        for j in range(M.cols):
            val = simplify(M[i, j])
            if val == 0 or val.is_zero:
                continue
            return False
    return True

def is_unitary(M):
    try:
        n = M.rows
        if M.cols != n:
            return False
        diff = M * M.H - eye(n)
        return is_zero_mat(diff)
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            U = witness['U']
            V = witness['V']
        else:
            U, V = witness
        
        if not isinstance(U, MatrixBase):
            U = Matrix(U)
        if not isinstance(V, MatrixBase):
            V = Matrix(V)
    except Exception:
        return [False, False]

    # H1: V is an n x n unitary matrix
    try:
        if not (U.is_square and V.is_square and U.rows == V.rows):
            h1 = False
        else:
            h1 = is_unitary(V)
    except Exception:
        h1 = False

    # neg_Q: W is NOT a unitary matrix
    try:
        if not (U.is_square and V.is_square and U.rows == V.rows):
            neg_q = False
        else:
            top = U.row_join(V)
            bottom = (-U).row_join(V)
            W = (1 / sqrt(2)) * top.col_join(bottom)
            neg_q = not is_unitary(W)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: V is an n x n unitary matrix",
    "¬Q: W is not a unitary matrix"
]

N_HYP = 1
NEG_Q_INDEX = 1