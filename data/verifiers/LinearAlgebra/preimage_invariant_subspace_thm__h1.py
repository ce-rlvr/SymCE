import sympy as sp

# Top-level setup for potential witness expressions
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    try:
        T, W = witness
    except Exception:
        return [False, False, False]
    
    # H_1: T is a linear operator on V
    try:
        h1 = isinstance(T, sp.Matrix) and T.is_square
        n = T.shape[0]
    except Exception:
        h1 = False
        n = 0

    # H_2: W is a T-invariant subspace of V
    try:
        if not h1:
            h2 = False
            W_mat = None
        else:
            if isinstance(W, sp.Matrix):
                W_mat = W
            elif isinstance(W, (list, tuple)):
                if len(W) == 0:
                    W_mat = sp.zeros(n, 1)
                elif isinstance(W[0], (list, tuple, sp.Matrix)):
                    cols = [sp.Matrix(w) if not isinstance(w, sp.Matrix) else w for w in W]
                    W_mat = sp.Matrix.hstack(*cols)
                else:
                    W_mat = sp.Matrix(W)
            else:
                W_mat = sp.Matrix(W)
            
            if W_mat.shape[0] != n:
                h2 = False
            else:
                rank_W = W_mat.rank()
                TW = T * W_mat
                W_TW = W_mat.row_join(TW)
                h2 = W_TW.rank() == rank_W
    except Exception:
        h2 = False
        W_mat = None

    # ¬Q: T^{-1}(W) is NOT a T-invariant subspace of V
    try:
        if not h1 or W_mat is None or W_mat.shape[0] != n:
            neg_q = False
        else:
            # Compute the preimage T^{-1}(W)
            # This is the set of vectors x such that T*x = W_mat*y for some y
            # Equivalently, [T, -W_mat] * [x; y] = 0
            M = T.row_join(-W_mat)
            null_basis = M.nullspace()
            
            if not null_basis:
                # Preimage is just the zero vector
                U = sp.zeros(n, 1)
            else:
                # Extract the first n components (the x part) from each basis vector
                U_cols = [v[:n, :] for v in null_basis]
                U = sp.Matrix.hstack(*U_cols)
            
            # Check if U (which spans T^{-1}(W)) is T-invariant
            rank_U = U.rank()
            TU = T * U
            U_TU = U.row_join(TU)
            is_invariant = U_TU.rank() == rank_U
            
            neg_q = not is_invariant
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: T is a linear operator on V",
    "H_2: W is a T-invariant subspace of V",
    "¬Q: T^{-1}(W) is not a T-invariant subspace of V"
]

N_HYP = 2
NEG_Q_INDEX = 2