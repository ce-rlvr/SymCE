import sympy
from sympy import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_pos_def(M):
    """Check if a real matrix is positive definite (i.e. its symmetric part is positive definite)."""
    if not M.is_square:
        return False
    sym_part = (M + M.T) / 2
    res = sym_part.is_positive_definite
    if res is not None:
        return res
    # Fallback for cases where is_positive_definite returns None
    try:
        evals = sym_part.eigenvals()
        for val in evals:
            if val.evalf() <= 0:
                return False
        return True
    except Exception:
        return False

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the given witness.
    The witness should be a tuple of two matrices: (A, B).
    """
    try:
        A, B = witness
    except Exception:
        return [False, False, False]
    
    # H_1: B is an m x m real positive definite matrix
    try:
        h1 = (isinstance(B, Matrix) and 
              B.is_square and 
              all(x.is_real == True for x in B) and 
              is_pos_def(B))
    except Exception:
        h1 = False

    # H_2: A is an n x n real matrix (implied by the Kronecker sum definition)
    try:
        h2 = (isinstance(A, Matrix) and 
              A.is_square and 
              all(x.is_real == True for x in A))
    except Exception:
        h2 = False

    # neg_Q: The Kronecker sum A \oplus B is NOT positive definite
    try:
        n = A.rows
        m = B.rows
        
        def kron(X, Y):
            return Matrix(X.rows * Y.rows, X.cols * Y.cols, 
                          lambda i, j: X[i // Y.rows, j // Y.cols] * Y[i % Y.rows, j % Y.cols])
        
        # A \oplus B = A \otimes I_m + I_n \otimes B
        A_oplus_B = kron(A, eye(m)) + kron(eye(n), B)
        
        neg_q = not is_pos_def(A_oplus_B)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: B is an m x m real positive definite matrix",
    "H_2: A is an n x n real matrix",
    "¬Q: The Kronecker sum A \oplus B is not positive definite"
]

N_HYP = 2
NEG_Q_INDEX = 2