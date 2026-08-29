import sympy
from sympy import Matrix, eye, zeros, I
from sympy.matrices import MatrixBase

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        h1 = isinstance(witness, MatrixBase) and witness.is_square
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            # If A = U * Sigma * U^T, then A^T = (U * Sigma * U^T)^T = U * Sigma^T * U^T = U * Sigma * U^T = A.
            # Thus, A must be symmetric for the factorization to exist.
            # By the Autonne-Takagi theorem, A is symmetric if and only if the factorization exists.
            # Therefore, the factorization does NOT exist if and only if A is NOT symmetric.
            neg_q = bool(witness != witness.T)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix with entries in C",
    "¬Q: There does not exist a unitary matrix U and a real non-negative diagonal matrix Sigma such that A = U Sigma U^T"
]

N_HYP = 1
NEG_Q_INDEX = 1