import sympy
from sympy import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness is expected to be a list of n x n sympy.Matrix objects spanning the subspace U,
    or a tuple (n, U) where U is a list of n x n matrices.
    """
    # H_1: V is the vector space of n x n matrices over a field F
    # We verify that the witness provides a valid collection of n x n matrices.
    try:
        if isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[0], int):
            n, U = witness
            h1 = isinstance(U, (list, tuple)) and all(hasattr(M, 'shape') and M.shape == (n, n) for M in U)
        else:
            U = witness
            if hasattr(U, 'shape'):
                U = [U]
            if not isinstance(U, (list, tuple)) or len(U) == 0:
                h1 = False
            else:
                n = U[0].shape[0]
                h1 = all(hasattr(M, 'shape') and M.shape == (n, n) for M in U)
    except Exception:
        h1 = False

    # ¬Q: U is NOT a subspace of V with dimension n(n+1)/2
    try:
        if not h1:
            neg_q = False
        else:
            if len(U) == 0:
                dim = 0
            else:
                # Flatten each matrix into a row vector to compute the dimension of their span
                rows = [list(M) for M in U]
                A = sympy.Matrix(rows)
                dim = A.rank()
            
            expected_dim = n * (n + 1) // 2
            neg_q = bool(dim != expected_dim)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: V is the vector space of n x n matrices over a field F",
    "¬Q: U is not a subspace of V with dimension n(n+1)/2"
]

N_HYP = 1
NEG_Q_INDEX = 1