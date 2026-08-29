import sympy
from sympy import Matrix, MatrixBase, eye, zeros
import math

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def max_sv(M):
    """
    Computes the maximum singular value of a SymPy matrix M.
    """
    if M.rows == 0 or M.cols == 0:
        return 0.0
    
    # Try using SymPy's built-in singular_values method first
    try:
        svs = M.singular_values()
        max_val = -1.0
        for val in svs:
            try:
                c = complex(val.evalf())
                v = c.real
                if v > max_val:
                    max_val = v
            except Exception:
                pass
        if max_val >= 0.0:
            return max_val
    except Exception:
        pass

    # Fallback to computing the square root of the maximum eigenvalue of M^H * M
    try:
        M_H_M = M.H * M
        evs = M_H_M.eigenvals()
        max_val = -1.0
        for val in evs.keys():
            try:
                c = complex(val.evalf())
                v = c.real
                if v > max_val:
                    max_val = v
            except Exception:
                pass
        if max_val < -1e-9:
            raise ValueError("Negative eigenvalue encountered for M.H * M")
        return math.sqrt(max(max_val, 0.0))
    except Exception:
        raise ValueError("Could not compute maximum singular value")

def conditions(witness):
    """
    Checks if the witness satisfies the hypotheses and violates the conclusion.
    Order of return: [H_1, H_2, neg_Q]
    """
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False, False]
        A, B = witness
    except Exception:
        return [False, False, False]

    # H_1: A is an m x n complex matrix
    try:
        if not isinstance(A, MatrixBase):
            A = Matrix(A)
        h1 = True
    except Exception:
        h1 = False

    # H_2: B is an n x p complex matrix (and dimensions match for multiplication)
    try:
        if not isinstance(B, MatrixBase):
            B = Matrix(B)
        h2 = (A.cols == B.rows) if h1 else False
    except Exception:
        h2 = False

    # neg_Q: The maximum singular value of AB is strictly greater than the product of their maximum singular values
    try:
        if h1 and h2:
            sv_AB = max_sv(A * B)
            sv_A = max_sv(A)
            sv_B = max_sv(B)
            # Using a small tolerance to account for floating-point inaccuracies
            neg_q = sv_AB > (sv_A * sv_B) + 1e-9
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is a complex matrix",
    "H_2: B is a complex matrix and A.cols == B.rows",
    "¬Q: The maximum singular value of AB is strictly greater than the product of their maximum singular values"
]

N_HYP = 2
NEG_Q_INDEX = 2