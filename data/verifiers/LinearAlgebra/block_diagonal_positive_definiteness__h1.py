import sympy
from sympy import Matrix, MatrixBase, diag, eye, zeros
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_pos_def(X):
    """Check if a real square matrix is positive definite using Sylvester's criterion."""
    if not X.is_symmetric():
        return False
    for i in range(1, X.rows + 1):
        det_val = X[:i, :i].det()
        try:
            if not (det_val > 0):
                return False
        except TypeError:
            # Cannot evaluate truth value (e.g., contains free symbols)
            return False
    return True

def is_real_matrix(X):
    """Check if all elements of the matrix are real numbers."""
    for v in X:
        if not v.is_real:
            return False
    return True

def conditions(witness):
    """
    Given a witness, checks if it satisfies the remaining hypotheses and falsifies the conclusion.
    The witness can be a tuple (A, B) or (A, B, M).
    """
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                A, B = witness
                if not isinstance(A, MatrixBase): A = Matrix(A)
                if not isinstance(B, MatrixBase): B = Matrix(B)
                M = diag(A, B)
            elif len(witness) == 3:
                A, B, M = witness
                if not isinstance(A, MatrixBase): A = Matrix(A)
                if not isinstance(B, MatrixBase): B = Matrix(B)
                if not isinstance(M, MatrixBase): M = Matrix(M)
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: Let B be an m \times m real positive definite matrix.
    try:
        h1 = B.is_square and B.rows >= 1 and is_real_matrix(B) and is_pos_def(B)
    except Exception:
        h1 = False

    # H_2: Let M be the (n+m) \times (n+m) block diagonal matrix with A and B as its diagonal blocks.
    # (This implies A must be an n \times n real matrix to form the block diagonal matrix M)
    try:
        h2 = A.is_square and A.rows >= 1 and is_real_matrix(A) and M == diag(A, B)
    except Exception:
        h2 = False

    # ¬Q: The block diagonal matrix M is NOT positive definite.
    try:
        neg_q = not is_pos_def(M)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: B is an m x m real positive definite matrix",
    "H_2: M is the (n+m) x (n+m) block diagonal matrix with A and B as its diagonal blocks",
    "¬Q: M is not positive definite"
]

N_HYP = 2
NEG_Q_INDEX = 2