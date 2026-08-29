import sympy as sp
from sympy import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_zero(e):
    """Helper to robustly check if a sympy expression is zero."""
    if e == 0:
        return True
    try:
        e_exp = sp.expand(e)
        if e_exp == 0:
            return True
        return sp.simplify(e_exp) == 0
    except Exception:
        return False

def conditions(witness):
    try:
        Q, W = witness
    except Exception:
        return [False, False, False]
        
    # H_1: Q is an n x n real orthogonal matrix
    try:
        Q = Matrix(Q)
        n = Q.rows
        if not Q.is_square:
            h1 = False
        else:
            diff = (Q.T * Q) - eye(n)
            h1 = all(is_zero(e) for e in diff)
            if h1:
                # Check if it contains explicit imaginary units
                if Q.has(sp.I):
                    h1 = False
    except Exception:
        h1 = False
        
    # H_2: W is invariant under Q
    W_mat = None
    try:
        h2 = True
        if isinstance(W, (list, tuple)):
            # W is provided as a set/list of vectors
            W_list = [Matrix(w) for w in W]
            for w in W_list:
                Qw = Q * w
                found = False
                for v in W_list:
                    diff = Qw - v
                    if all(is_zero(e) for e in diff):
                        found = True
                        break
                if not found:
                    h2 = False
                    break
            if W_list:
                W_mat = Matrix.hstack(*W_list)
            else:
                W_mat = Matrix(n, 0, [])
        else:
            # W is provided as a matrix whose columns span the subspace
            W_mat = Matrix(W)
            if W_mat.rows != n:
                if W_mat.cols == n:
                    W_mat = W_mat.T
                else:
                    h2 = False
            if h2:
                rank_W = W_mat.rank()
                for i in range(W_mat.cols):
                    w = W_mat[:, i]
                    if W_mat.row_join(Q * w).rank() > rank_W:
                        h2 = False
                        break
    except Exception:
        h2 = False
        
    # ¬Q: W^\perp is NOT invariant under Q
    try:
        if W_mat is None:
            neg_q = False
        else:
            # W^\perp is the nullspace of W_mat.T
            W_perp = W_mat.T.nullspace()
            concl = True
            for v in W_perp:
                # Check if Q*v is in W^\perp (i.e., orthogonal to all columns of W_mat)
                prod = W_mat.T * (Q * v)
                if not all(is_zero(e) for e in prod):
                    concl = False
                    break
            neg_q = not concl
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: Q is an n x n real orthogonal matrix",
    "H_2: W is invariant under Q",
    "¬Q: W^\\perp is not invariant under Q"
]

N_HYP = 2
NEG_Q_INDEX = 2