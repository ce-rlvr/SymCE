import sympy
from sympy import eye, zeros, diag, Matrix, simplify

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_unitary(mat):
    try:
        if not getattr(mat, 'is_square', False):
            return False
        I = eye(mat.rows)
        diff = mat * mat.H - I
        
        if diff.is_zero_matrix:
            return True
        if diff.expand().is_zero_matrix:
            return True
        if simplify(diff).is_zero_matrix:
            return True
            
        for i in range(diff.rows):
            for j in range(diff.cols):
                val = diff[i, j]
                if val == 0 or getattr(val, 'is_zero', False):
                    continue
                if simplify(val) == 0:
                    continue
                return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        A, B = witness
        if not isinstance(A, sympy.MatrixBase):
            A = Matrix(A)
        if not isinstance(B, sympy.MatrixBase):
            B = Matrix(B)
    except Exception:
        return [False, False, False]

    # H_1: B is an m x m complex unitary matrix
    try:
        h1_ok = is_unitary(B)
    except Exception:
        h1_ok = False

    # H_2: M is the (n+m) x (n+m) block diagonal matrix with diagonal blocks A and B
    # This requires A to be a square matrix (n x n)
    try:
        h2_ok = getattr(A, 'is_square', False)
    except Exception:
        h2_ok = False

    # ¬Q: M is NOT a unitary matrix
    try:
        if h2_ok:
            M = diag(A, B)
            neg_q_ok = not is_unitary(M)
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: B is an m x m complex unitary matrix",
    "H_2: M is the (n+m) x (n+m) block diagonal matrix with diagonal blocks A and B",
    "¬Q: M is not a unitary matrix"
]

N_HYP = 2
NEG_Q_INDEX = 2