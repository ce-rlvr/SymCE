import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 3:
            return [False, False]
        A, lam, mu = witness
    except Exception:
        return [False, False]

    try:
        h1 = isinstance(A, sympy.MatrixBase) and A.rows == A.cols and A.rows > 0
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            n = A.rows
            I = eye(n)
            # Generalized eigenspace for lambda is the nullspace of (A - lambda*I)^n
            M_lam = (A - lam * I)**n
            # Generalized eigenspace for mu is the nullspace of (A - mu*I)^n
            M_mu = (A - mu * I)**n
            
            # The intersection of their nullspaces is the nullspace of the vertically stacked matrix
            M_stacked = M_lam.col_join(M_mu)
            
            # The intersection contains a non-zero vector iff the nullspace is non-trivial
            # i.e., the rank of the stacked matrix is strictly less than n
            neg_q = bool(M_stacked.rank() < n)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix over a field F",
    "¬Q: The intersection of the generalized eigenspaces for lambda and mu contains a non-zero vector"
]

N_HYP = 1
NEG_Q_INDEX = 1