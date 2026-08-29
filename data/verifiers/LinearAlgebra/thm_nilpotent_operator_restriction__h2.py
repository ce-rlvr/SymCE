import sympy
from sympy import Matrix, zeros, eye

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def nilpotency_index(M):
    """Returns the index of nilpotency of a square matrix M, or float('inf') if not nilpotent."""
    if M.rows == 0:
        return 1
    k = 1
    Mk = M
    while k <= M.rows:
        if Mk.is_zero_matrix:
            return k
        Mk = Mk * M
        k += 1
    return float('inf')

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the Nilpotent Operator Restriction Theorem.
    Witness is expected to be a tuple (T, W) where T is the operator matrix and W is a matrix 
    whose columns span the subspace.
    """
    # H1: V is a vector space (T is a square matrix, W is a matrix with compatible rows)
    try:
        T, W = witness
        if isinstance(W, (list, tuple)):
            if len(W) == 0:
                W = zeros(T.rows, 0)
            else:
                W = Matrix.hstack(*W)
        h1 = isinstance(T, Matrix) and isinstance(W, Matrix) and T.is_square and T.rows == W.rows
    except Exception:
        h1 = False

    # H2: W is a T-invariant subspace of V
    try:
        if not h1:
            h2 = False
        else:
            B_cols = W.columnspace()
            if not B_cols:
                B = zeros(T.rows, 0)
            else:
                B = Matrix.hstack(*B_cols)
            
            if B.cols == 0:
                h2 = True
            else:
                TB = T * B
                augmented = Matrix.hstack(B, TB)
                h2 = (B.rank() == augmented.rank())
    except Exception:
        h2 = False

    # neg_Q: The conclusion FAILS.
    # Conclusion: T|_W is nilpotent, and its index of nilpotency is <= index of nilpotency of T.
    try:
        if not h1 or not h2:
            neg_q = False
        else:
            B_cols = W.columnspace()
            if not B_cols:
                B = zeros(T.rows, 0)
            else:
                B = Matrix.hstack(*B_cols)
                
            if B.cols == 0:
                index_TW = 1
            else:
                # A is the matrix of T|_W with respect to the basis B
                A = (B.T * B).inv() * B.T * T * B
                index_TW = nilpotency_index(A)
                
            index_T = nilpotency_index(T)
            
            if index_T == float('inf'):
                # If T is not nilpotent, it has no index of nilpotency.
                # The conclusion refers to "the index of nilpotency of T", which fails to exist.
                q = False
            else:
                q = (index_TW != float('inf')) and (index_TW <= index_T)
                
            neg_q = not q
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: V is a vector space (T is an operator, W is a subspace)",
    "H_2: W is a T-invariant subspace of V",
    "¬Q: T|_W is not nilpotent, or its index of nilpotency is greater than that of T (or T is not nilpotent)"
]

N_HYP = 2
NEG_Q_INDEX = 2