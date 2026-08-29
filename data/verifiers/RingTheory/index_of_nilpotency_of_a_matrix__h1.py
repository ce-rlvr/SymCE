import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x, y, z

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_zero_mat(M):
    """Helper function to robustly check if a matrix or scalar is zero."""
    if hasattr(M, 'is_zero_matrix') and M.is_zero_matrix is not None:
        return M.is_zero_matrix
    if hasattr(M, 'is_zero') and M.is_zero is not None:
        return M.is_zero
    if hasattr(M, 'as_explicit'):
        try:
            M_exp = M.as_explicit()
            if hasattr(M_exp, 'is_zero_matrix') and M_exp.is_zero_matrix is not None:
                return M_exp.is_zero_matrix
        except Exception:
            pass
    try:
        for e in M:
            if isinstance(e, (list, tuple, set)):
                if not is_zero_mat(e):
                    return False
            else:
                if e != 0:
                    if hasattr(e, 'is_zero') and e.is_zero:
                        continue
                    return False
        return True
    except TypeError:
        return M == 0

def conditions(witness) -> list[bool]:
    # H_1: A is an n \times n matrix over F
    h1 = False
    n = 0
    try:
        shape = witness.shape
        if len(shape) == 2 and shape[0] == shape[1]:
            h1 = True
            n = shape[0]
    except Exception:
        h1 = False

    # H_2: A is a nilpotent matrix
    h2 = False
    try:
        if h1:
            curr = witness
            # Check up to a reasonable power for nilpotency
            for _ in range(1, n + 100):
                if is_zero_mat(curr):
                    h2 = True
                    break
                curr = curr * witness
    except Exception:
        h2 = False

    # ¬Q: A^n is NOT the zero matrix
    neg_q = False
    try:
        if h1:
            A_n = witness
            for _ in range(n - 1):
                A_n = A_n * witness
            
            # For n=0, A^0 is the identity matrix, which is a 0x0 matrix (thus zero)
            if n == 0:
                neg_q = not is_zero_mat(zeros(0, 0))
            else:
                if not is_zero_mat(A_n):
                    neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix",
    "H_2: A is a nilpotent matrix",
    "¬Q: A^n is not the zero matrix"
]

N_HYP = 2
NEG_Q_INDEX = 2