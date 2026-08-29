import sympy
from sympy import Matrix, eye, zeros

# Top-level setup: named object bindings that the witness expression may reference.
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks whether it is a valid counterexample.
    The witness is expected to be a list or tuple of matrices representing the linear maps f_1, ..., f_k.
    """
    # H_1: V is an n-dimensional vector space over a field F
    # We verify this by checking that the witness is a non-empty list of matrices,
    # all of which have the same number of columns (n).
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) == 0:
            h1_ok = False
        else:
            matrices = [Matrix(A) for A in witness]
            n = matrices[0].cols
            h1_ok = all(A.cols == n for A in matrices)
    except Exception:
        h1_ok = False

    # neg_Q: The dimension of the intersection of the kernels of f_1, ..., f_k is less than n - k
    try:
        matrices = [Matrix(A) for A in witness]
        k = len(matrices)
        n = matrices[0].cols
        
        # The intersection of the kernels is the nullspace of the vertically stacked matrix
        M = Matrix.vstack(*matrices)
        
        # By Rank-Nullity, the dimension of the nullspace is n - rank(M)
        dim_intersection = n - M.rank()
        
        # The conclusion fails if this dimension is strictly less than n - k
        neg_q_ok = bool(dim_intersection < n - k)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: V is an n-dimensional vector space over a field F (witness is a list of matrices with n columns)",
    "¬Q: The dimension of the intersection of the kernels of f_1, ..., f_k is less than n - k"
]

N_HYP = 1
NEG_Q_INDEX = 1