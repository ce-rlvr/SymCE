import sympy
from sympy import Matrix, eye, zeros
import math

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Given a witness (which should be a tuple (D, X) where D is a sympy Matrix 
    and X is a list of vectors/points), checks if it is a valid counterexample.
    """
    try:
        D, X = witness
    except Exception:
        return [False, False]

    # H_1: D is the n x n matrix with entries D_{ij} = ||x_i - x_j||^2
    h1_ok = False
    try:
        if isinstance(D, Matrix) and isinstance(X, list) and len(X) > 0:
            n = len(X)
            if D.shape == (n, n):
                is_edm = True
                for i in range(n):
                    for j in range(n):
                        diff = [a - b for a, b in zip(X[i], X[j])]
                        sq_dist = sum(comp**2 for comp in diff)
                        if sympy.simplify(D[i, j] - sq_dist) != 0:
                            is_edm = False
                            break
                    if not is_edm:
                        break
                h1_ok = is_edm
    except Exception:
        h1_ok = False

    # neg_Q: The Euclidean distance matrix D is NOT orthogonally diagonalizable over the real numbers.
    # Note: Any real symmetric matrix is orthogonally diagonalizable over the real numbers.
    # If D is an EDM, it is symmetric, so it is always orthogonally diagonalizable.
    # Thus, neg_Q will be False for any valid EDM. We check if D is NOT symmetric or has non-real eigenvalues.
    neg_q_ok = False
    try:
        if isinstance(D, Matrix):
            if not D.is_symmetric():
                neg_q_ok = True
            else:
                # A real symmetric matrix is always orthogonally diagonalizable.
                # We check if it's not diagonalizable or has non-real eigenvalues.
                if not D.is_diagonalizable(reals_only=True):
                    neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: D is the n x n matrix with entries D_{ij} = ||x_i - x_j||^2, where ||.|| is the Euclidean norm",
    "¬Q: The Euclidean distance matrix D is not orthogonally diagonalizable over the real numbers"
]

N_HYP = 1
NEG_Q_INDEX = 1