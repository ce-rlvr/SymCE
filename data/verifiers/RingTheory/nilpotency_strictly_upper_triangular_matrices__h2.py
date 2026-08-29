import sympy
from sympy import Matrix, zeros, eye, expand
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: U is the ring of n by n strictly upper triangular matrices with entries in R",
    "H_3: A is a matrix in U",
    "¬Q: A^n is not the zero matrix"
]

N_HYP = 3
NEG_Q_INDEX = 3

def is_zero(expr):
    """Helper to robustly check if a sympy expression is zero."""
    try:
        if expr == 0:
            return True
        return expand(expr) == 0
    except Exception:
        return False

def conditions(witness):
    # Extract the matrix A from the witness
    try:
        if isinstance(witness, tuple):
            A = witness[-1]
        else:
            A = witness
            
        # Convert to sympy Matrix if it's not already one (e.g., list of lists)
        if not hasattr(A, 'rows'):
            A = Matrix(A)
            
        n = A.rows
        cols = A.cols
    except Exception:
        return [False, False, False, False]

    # H_1: R is a commutative ring
    try:
        h1 = True
        for val in A:
            if hasattr(val, 'is_commutative') and val.is_commutative is False:
                h1 = False
                break
    except Exception:
        h1 = False

    # H_2: U is the ring of n by n strictly upper triangular matrices with entries in R
    # This is a definitional hypothesis. If A is a valid matrix, such a ring U exists.
    try:
        h2 = True if hasattr(A, 'rows') and hasattr(A, 'cols') else False
    except Exception:
        h2 = False

    # H_3: A is a matrix in U (i.e., A is an n x n strictly upper triangular matrix)
    try:
        h3 = False
        if A.is_square:
            h3 = True
            for i in range(A.rows):
                for j in range(i + 1):
                    if not is_zero(A[i, j]):
                        h3 = False
                        break
                if not h3:
                    break
    except Exception:
        h3 = False

    # ¬Q: A^n is not the zero matrix
    try:
        An = A**n
        neg_q = False
        for i in range(n):
            for j in range(n):
                if not is_zero(An[i, j]):
                    neg_q = True
                    break
            if neg_q:
                break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]