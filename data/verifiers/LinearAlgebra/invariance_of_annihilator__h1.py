import sympy as sp

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    try:
        T, W = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = isinstance(T, sp.MatrixBase) and T.is_square
    except Exception:
        h1 = False
        
    try:
        if isinstance(W, (list, tuple, set)):
            W_list = list(W)
            if len(W_list) > 0:
                W_mat = sp.Matrix.hstack(*[sp.Matrix(w) for w in W_list])
            else:
                if h1:
                    W_mat = sp.zeros(T.rows, 0)
                else:
                    W_mat = sp.zeros(0, 0)
        else:
            W_mat = W
            
        if not isinstance(W_mat, sp.MatrixBase):
            h2 = False
        elif not h1 or W_mat.rows != T.rows:
            h2 = False
        else:
            rank_W = W_mat.rank()
            aug = sp.Matrix.hstack(W_mat, T * W_mat)
            h2 = aug.rank() == rank_W
    except Exception:
        h2 = False
        
    try:
        if not h1 or not isinstance(W_mat, sp.MatrixBase) or W_mat.rows != T.rows:
            neg_q = False
        else:
            # W^0 is the annihilator, represented by the left nullspace of W (nullspace of W.T)
            W0_basis = W_mat.T.nullspace()
            is_invariant = True
            
            # T^* is the dual operator, represented by the transpose of T
            T_star = T.T
            
            for f in W0_basis:
                # Check if T^*(f) is in W^0
                # f is in W^0 iff W_mat.T * f == 0
                # So T^*(f) is in W^0 iff W_mat.T * (T_star * f) == 0
                prod = W_mat.T * (T_star * f)
                prod = sp.simplify(prod)
                if not prod.is_zero_matrix:
                    is_invariant = False
                    break
                    
            neg_q = not is_invariant
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: T is a linear operator on V",
    "H_2: W is a T-invariant subspace of V",
    "¬Q: W^0 is not a T^*-invariant subspace of V^*"
]

N_HYP = 2
NEG_Q_INDEX = 2