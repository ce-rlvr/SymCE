import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        n, S = witness
    except Exception:
        return [False, False, False]

    # H_1: n is a positive integer
    try:
        n_int = int(n)
        h1 = isinstance(n, (int, sympy.Integer)) and n_int > 0
    except Exception:
        h1 = False

    # H_2: S is a subspace of the vector space of n x n matrices
    # (represented as a collection of n x n matrices that span the subspace)
    try:
        n_int = int(n)
        h2 = isinstance(S, (list, tuple, set)) and all(
            hasattr(M, 'shape') and M.shape == (n_int, n_int) for M in S
        )
    except Exception:
        h2 = False

    # ¬Q: The dimension of S is not n(n+1)/2
    try:
        n_int = int(n)
        if not S:
            dim = 0
        else:
            # Flatten each matrix into a row vector to form a matrix of basis vectors
            vectors = [list(sympy.Matrix(M)) for M in S]
            A = sympy.Matrix(vectors)
            dim = A.rank()
        
        expected_dim = n_int * (n_int + 1) // 2
        neg_q = dim != expected_dim
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: S is a subspace of the vector space of n x n matrices",
    "¬Q: The dimension of S is not n(n+1)/2"
]

N_HYP = 2
NEG_Q_INDEX = 2