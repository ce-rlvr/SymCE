import sympy as sp
from sympy import Matrix, zeros, eye

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness must provide both the matrix A and the integer n.
    """
    try:
        if isinstance(witness, dict):
            A = witness['A']
            n = witness['n']
        elif hasattr(witness, 'A') and hasattr(witness, 'n'):
            A = witness.A
            n = witness.n
        else:
            A, n = witness
    except Exception:
        return [False, False, False]

    # H_1: F is a field (A is a matrix over a field)
    try:
        h1 = isinstance(A, Matrix) and A.is_square
    except Exception:
        h1 = False

    # H_2: A is nilpotent
    # An m x m matrix is nilpotent iff A^m is the zero matrix.
    try:
        if h1:
            m = A.shape[0]
            h2 = bool(A**m == zeros(m, m))
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: A^n is NOT equal to the n x n zero matrix
    try:
        if h1 and isinstance(n, (int, sp.Integer)) and n > 0:
            neg_q = bool(A**n != zeros(n, n))
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: A is nilpotent",
    "¬Q: A^n is not equal to the n x n zero matrix"
]

N_HYP = 2
NEG_Q_INDEX = 2