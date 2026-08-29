import sympy
from sympy import MatrixBase, eye, simplify, zeros
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_zero_mat(M):
    if getattr(M, 'is_zero_matrix', None) is True:
        return True
    try:
        M_simp = simplify(M)
        if getattr(M_simp, 'is_zero_matrix', None) is True:
            return True
        for i in range(M_simp.rows):
            for j in range(M_simp.cols):
                if simplify(M_simp[i, j]) != 0:
                    return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        h1 = isinstance(witness, MatrixBase) and witness.rows == witness.cols
    except Exception:
        h1 = False

    try:
        if not h1:
            h2 = False
        else:
            n = witness.rows
            diff = witness * witness.H - eye(n)
            h2 = is_zero_mat(diff)
    except Exception:
        h2 = False

    try:
        if not h1:
            neg_q = False
        else:
            n = witness.rows
            diff = witness * witness.T - eye(n)
            is_ortho = is_zero_mat(diff)
            neg_q = not is_ortho
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: U is a square matrix over the complex numbers",
    "H_2: U is a unitary matrix",
    "¬Q: U is not an orthogonal matrix"
]

N_HYP = 2
NEG_Q_INDEX = 2