import sympy as sp
from sympy.matrices import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the false conjecture:
    'Nilpotency of Strictly Upper Triangular Matrices' (with a dropped hypothesis).
    """
    try:
        # The witness can be a tuple (A, n) or just the matrix A (where n is inferred as its dimension)
        if isinstance(witness, tuple):
            A, n = witness
        else:
            A = witness
            n = A.shape[0]
    except Exception:
        return [False, False, False, False]
        
    # H_1: R is a commutative ring
    try:
        # Check if A is a sympy Matrix and all its elements belong to a commutative ring
        h1 = bool(isinstance(A, Matrix) and all(getattr(x, 'is_commutative', True) for x in A))
    except Exception:
        h1 = False
        
    # H_2: n is a positive integer
    try:
        h2 = bool(isinstance(n, (int, sp.Integer)) and n > 0)
    except Exception:
        h2 = False
        
    # H_3: A is a matrix in U
    try:
        # U represents the set of upper triangular matrices.
        # (If the dropped hypothesis was "strictly", A being upper triangular is sufficient to satisfy this remaining hypothesis).
        h3 = bool(A.is_square and A.is_upper)
    except Exception:
        h3 = False
        
    # ¬Q: A^n is not the zero matrix (and thus A is not necessarily nilpotent of degree n)
    try:
        An = A**n
        neg_q = bool(An != zeros(A.shape[0], A.shape[1]))
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: n is a positive integer",
    "H_3: A is a matrix in U",
    "¬Q: A^n is not the zero matrix"
]

N_HYP = 3
NEG_Q_INDEX = 3