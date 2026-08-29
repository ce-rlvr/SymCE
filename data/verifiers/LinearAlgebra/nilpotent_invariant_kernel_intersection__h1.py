import sympy
from sympy import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_matrix(obj):
    if isinstance(obj, Matrix):
        return obj
    if isinstance(obj, list):
        if len(obj) == 0:
            return Matrix()
        if isinstance(obj[0], Matrix):
            return Matrix.hstack(*obj)
    return Matrix(obj)

def conditions(witness):
    # witness is expected to be a tuple (T, W)
    # T is the matrix of the linear operator
    # W is a matrix whose columns span the subspace, or a list of column vectors
    
    try:
        T = get_matrix(witness[0])
        n = T.shape[0]
        h1 = (T.shape[0] == T.shape[1]) and (T**n).is_zero_matrix
    except Exception:
        h1 = False

    try:
        T = get_matrix(witness[0])
        W = get_matrix(witness[1])
        if W.shape[0] != T.shape[1]:
            h2 = False
        else:
            is_nonzero = (W.shape[1] > 0) and not W.is_zero_matrix
            if not is_nonzero:
                h2 = False
            else:
                W_rank = W.rank()
                is_invariant = True
                for i in range(W.shape[1]):
                    col = W[:, i]
                    T_col = T * col
                    if W.row_join(T_col).rank() > W_rank:
                        is_invariant = False
                        break
                h2 = is_invariant
    except Exception:
        h2 = False

    try:
        T = get_matrix(witness[0])
        W = get_matrix(witness[1])
        if W.shape[0] != T.shape[1]:
            neg_q = False
        else:
            # Intersection of W and ker(T)
            # x in W \cap ker(T) iff x = W*v and T*x = 0
            # So T*W*v = 0, meaning v is in ker(T*W)
            TW = T * W
            N = TW.nullspace()
            if not N:
                # ker(T*W) is trivial, so W \cap ker(T) = {0}
                neg_q = True
            else:
                N_mat = Matrix.hstack(*N)
                int_gen = W * N_mat
                # If int_gen is the zero matrix, all such x are 0
                neg_q = int_gen.is_zero_matrix
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: T is a nilpotent linear operator",
    "H_2: W is a non-zero T-invariant subspace of V",
    "¬Q: W \\cap \\ker(T) = {0}"
]

N_HYP = 2
NEG_Q_INDEX = 2