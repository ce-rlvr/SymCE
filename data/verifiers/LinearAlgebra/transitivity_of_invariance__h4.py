import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_columns(M):
    if isinstance(M, (list, tuple)):
        return list(M)
    elif isinstance(M, Matrix):
        return [M[:, i] for i in range(M.cols)]
    return []

def in_span(v, basis):
    if not basis:
        return all(val == 0 for val in v)
    M = Matrix.hstack(*basis)
    M_v = Matrix.hstack(M, v)
    return M.rank() == M_v.rank()

def is_subset(W, U):
    for w in W:
        if not in_span(w, U):
            return False
    return True

def is_invariant(T, W):
    for w in W:
        if not in_span(T * w, W):
            return False
    return True

def conditions(witness):
    try:
        T, U, W = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        if not isinstance(T, Matrix) or not T.is_square:
            h1_ok = False
        else:
            n = T.rows
            U_cols = get_columns(U)
            W_cols = get_columns(W)
            h1_ok = True
            for v in U_cols + W_cols:
                if not isinstance(v, Matrix) or v.shape != (n, 1):
                    h1_ok = False
                    break
    except Exception:
        h1_ok = False

    try:
        h2_ok = isinstance(T, Matrix) and T.is_square
    except Exception:
        h2_ok = False

    try:
        U_cols = get_columns(U)
        h3_ok = is_invariant(T, U_cols)
    except Exception:
        h3_ok = False

    try:
        U_cols = get_columns(U)
        W_cols = get_columns(W)
        
        # W is invariant under T
        w_inv_t = is_invariant(T, W_cols)
        
        # W is invariant under T|_U (requires W to be a subspace of U)
        w_inv_tu = is_subset(W_cols, U_cols) and w_inv_t
        
        # The conclusion claims they are equivalent. The negation means they are not.
        neg_q_ok = bool(w_inv_tu != w_inv_t)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: V is a vector space",
    "H_2: T is a linear operator on V",
    "H_3: U is a T-invariant subspace of V",
    "¬Q: W is invariant under T|_U iff W is invariant under T fails"
]

N_HYP = 3
NEG_Q_INDEX = 3