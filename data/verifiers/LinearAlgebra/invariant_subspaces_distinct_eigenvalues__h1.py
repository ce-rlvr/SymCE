import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # Unpack witness: can be a tuple (T, n) or just the matrix T
    try:
        if isinstance(witness, tuple):
            T, n = witness
        else:
            T = witness
            n = len(T.eigenvals()) if hasattr(T, 'eigenvals') else None
    except Exception:
        T = witness
        n = None

    # H_1: T is a linear operator on V
    try:
        h1 = isinstance(T, Matrix) and T.is_square
    except Exception:
        h1 = False

    # H_2: T has n distinct eigenvalues
    try:
        evs = T.eigenvals()
        h2 = (len(evs) == n)
    except Exception:
        h2 = False

    # ¬Q: The conclusion states "Every T-invariant subspace of V is spanned by a subset 
    # of the eigenvectors of T."
    # This holds if and only if T is diagonalizable. If T is not diagonalizable, 
    # there exists a generalized eigenvector that forms a T-invariant subspace 
    # (along with the regular eigenvector) which is NOT spanned by eigenvectors.
    # Therefore, the conclusion FAILS (neg_Q is True) iff T is NOT diagonalizable.
    try:
        neg_q = not T.is_diagonalizable()
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: T is a linear operator on V",
    "H_2: T has n distinct eigenvalues",
    "¬Q: There exists a T-invariant subspace not spanned by eigenvectors of T"
]

N_HYP = 2
NEG_Q_INDEX = 2