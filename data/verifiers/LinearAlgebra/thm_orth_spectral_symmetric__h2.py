import sympy
from sympy import Matrix, eye, zeros

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: A is a real n x n matrix
    try:
        A = Matrix(witness)
        h1 = bool(A.is_square and all(e.is_real == True for e in A))
    except Exception:
        h1 = False

    # ¬Q: There do not exist real orthogonal Q and real diagonal D such that A = Q D Q^T.
    # Since Q D Q^T is always symmetric for any diagonal D and orthogonal Q, 
    # A can only be written in this form if A is symmetric.
    # By the Spectral Theorem, every real symmetric matrix can be written in this form.
    # Thus, the conclusion fails if and only if A is NOT symmetric.
    try:
        A = Matrix(witness)
        neg_q = not bool(A.is_symmetric())
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is a real n x n matrix",
    "¬Q: There do not exist real orthogonal Q and real diagonal D such that A = Q D Q^T (A is not symmetric)"
]

N_HYP = 1
NEG_Q_INDEX = 1