import sympy
from sympy import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        T, W = witness
    except Exception:
        return [False, False, False]
        
    # H1: T is a nilpotent linear operator on V
    try:
        n = T.shape[0]
        if T.shape[0] != T.shape[1]:
            h1 = False
        else:
            T_pow = T**n
            h1 = (getattr(T_pow, 'is_zero_matrix', None) == True)
            if not h1:
                try:
                    h1 = (getattr(sympy.simplify(T_pow), 'is_zero_matrix', None) == True)
                except Exception:
                    pass
    except Exception:
        h1 = False

    # H2: W is a T-invariant subspace of V
    try:
        if isinstance(W, list):
            if len(W) == 0:
                W_mat = sympy.zeros(T.shape[0], 1)
            else:
                cols = []
                for x in W:
                    vec = sympy.Matrix(x)
                    if vec.shape[0] == 1:
                        vec = vec.T
                    cols.append(vec)
                W_mat = sympy.Matrix.hstack(*cols)
        else:
            W_mat = sympy.Matrix(W)
            
        if W_mat.shape[0] != T.shape[0]:
            h2 = False
        else:
            rank_W = W_mat.rank()
            TW_mat = T * W_mat
            rank_TW = W_mat.row_join(TW_mat).rank()
            h2 = (rank_W == rank_TW)
    except Exception:
        h2 = False
        W_mat = None

    # neg_Q: The quotient operator T/W is not nilpotent
    try:
        if W_mat is None or W_mat.shape[0] != T.shape[0]:
            neg_q = False
        else:
            n = T.shape[0]
            W_basis = W_mat.columnspace()
            if not W_basis:
                T_pow = T**n
                is_q_nil = (getattr(T_pow, 'is_zero_matrix', None) == True)
                if not is_q_nil:
                    try:
                        is_q_nil = (getattr(sympy.simplify(T_pow), 'is_zero_matrix', None) == True)
                    except Exception:
                        pass
            else:
                B_W = sympy.Matrix.hstack(*W_basis)
                r = B_W.shape[1]
                if r == n:
                    is_q_nil = True
                else:
                    M = B_W.row_join(sympy.eye(n))
                    _, pivots = M.rref()
                    B = M[:, list(pivots)]
                    T_mat = T if isinstance(T, sympy.Matrix) else sympy.Matrix(T)
                    T_B = B.inv() * T_mat * B
                    T_Q = T_B[r:, r:]
                    T_Q_pow = T_Q**(n - r)
                    is_q_nil = (getattr(T_Q_pow, 'is_zero_matrix', None) == True)
                    if not is_q_nil:
                        try:
                            is_q_nil = (getattr(sympy.simplify(T_Q_pow), 'is_zero_matrix', None) == True)
                        except Exception:
                            pass
            neg_q = not is_q_nil
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: T is a nilpotent linear operator on V",
    "H_2: W is a T-invariant subspace of V",
    "¬Q: The quotient operator T/W is not nilpotent"
]

N_HYP = 2
NEG_Q_INDEX = 2