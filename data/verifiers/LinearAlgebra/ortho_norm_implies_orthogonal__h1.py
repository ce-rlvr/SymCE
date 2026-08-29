import sympy
from sympy import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: For every vector x in R^n, the Euclidean norm of Ax equals the Euclidean norm of x
    try:
        A = sympy.Matrix(witness)
        n = A.cols
        # For a real matrix A, ||Ax|| = ||x|| for all x in R^n iff A^T A = I_n
        h1 = (A.T * A == sympy.eye(n))
        h1 = h1 and all(e.is_real for e in A)
    except Exception:
        h1 = False

    # neg_Q: A is NOT an orthogonal matrix
    try:
        A = sympy.Matrix(witness)
        n = A.cols
        # An orthogonal matrix must be square, real, and satisfy A^T A = I
        is_orthogonal = A.is_square and (A.T * A == sympy.eye(n)) and all(e.is_real for e in A)
        neg_q = not is_orthogonal
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: For every vector x in R^n, the Euclidean norm of Ax equals the Euclidean norm of x",
    "¬Q: A is not an orthogonal matrix"
]

N_HYP = 1
NEG_Q_INDEX = 1