import sympy as sp

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 3:
            T, W, v = witness
        elif len(witness) == 4:
            V, T, W, v = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: V is a vector space over a field F
    try:
        h1 = isinstance(T, sp.Matrix) and T.is_square
    except Exception:
        h1 = False

    # H2: T is a linear operator on V
    try:
        h2 = h1
    except Exception:
        h2 = False

    W_mat = None
    # H3: W is a T-invariant subspace of V
    try:
        n = T.shape[0]
        h3 = False
        if isinstance(W, sp.Matrix):
            if W.shape[0] == n:
                W_mat = W
                h3 = True
        elif isinstance(W, (list, tuple)):
            h3 = True
            for w in W:
                if not (isinstance(w, sp.Matrix) and w.shape == (n, 1)):
                    h3 = False
                    break
            if h3:
                if len(W) > 0:
                    W_mat = sp.Matrix.hstack(*W)
                else:
                    W_mat = sp.zeros(n, 1)
        
        if h3 and W_mat is not None:
            if W_mat.is_zero_matrix:
                pass
            else:
                TW_mat = T * W_mat
                if W_mat.rank() != W_mat.row_join(TW_mat).rank():
                    h3 = False
    except Exception:
        h3 = False

    # neg_Q: S_T(v; W) is not an ideal
    try:
        n = T.shape[0]
        # If v is not an n x 1 matrix, it's not in V, so S_T(v; W) is not an ideal
        if not (isinstance(v, sp.Matrix) and v.shape == (n, 1)):
            neg_q = True
        else:
            neg_q = False
    except Exception:
        neg_q = True

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: V is a vector space over a field F",
    "H_2: T is a linear operator on V",
    "H_3: W is a T-invariant subspace of V",
    "not Q: S_T(v; W) is not an ideal"
]

N_HYP = 3
NEG_Q_INDEX = 3