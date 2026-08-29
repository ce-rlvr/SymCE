import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def _is_zero_mat(M):
    if M.is_zero_matrix:
        return True
    M_exp = M.expand()
    if M_exp.is_zero_matrix:
        return True
    M_simp = sympy.simplify(M_exp)
    if M_simp.is_zero_matrix:
        return True
    try:
        return all(abs(complex(val)) < 1e-9 for val in M.evalf())
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 2:
            return [False, False]
        U, x = witness
    except Exception:
        return [False, False]

    try:
        U_mat = Matrix(U)
        x_mat = Matrix(x)
    except Exception:
        return [False, False]

    # H_1: U is an n x n unitary matrix
    try:
        if U_mat.rows != U_mat.cols:
            h1 = False
        elif not ((x_mat.rows == U_mat.rows and x_mat.cols == 1) or 
                  (x_mat.cols == U_mat.rows and x_mat.rows == 1)):
            h1 = False
        else:
            n = U_mat.rows
            diff = U_mat.H * U_mat - eye(n)
            h1 = _is_zero_mat(diff)
    except Exception:
        h1 = False

    # neg_Q: x != 0
    try:
        neg_q = not _is_zero_mat(x_mat)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: U is an n x n unitary matrix",
    "¬Q: x != 0"
]

N_HYP = 1
NEG_Q_INDEX = 1