import sympy
from sympy import Matrix, MatrixBase, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False] * 5
        T, W = witness
        if not isinstance(T, MatrixBase):
            return [False] * 5
        if isinstance(W, (list, tuple)):
            if len(W) > 0:
                if isinstance(W[0], (int, float, complex, sympy.Expr)):
                    W = T.__class__(W)
                else:
                    W_mats = [w if isinstance(w, MatrixBase) else T.__class__(w) for w in W]
                    W = T.__class__.hstack(*W_mats)
            else:
                W = T.__class__.zeros(T.shape[0], 0)
        elif not isinstance(W, MatrixBase):
            return [False] * 5
    except Exception:
        return [False] * 5

    try:
        h1 = isinstance(T, MatrixBase) and isinstance(W, MatrixBase)
    except Exception:
        h1 = False

    try:
        h2 = T.is_square and W.shape[0] == T.shape[0]
    except Exception:
        h2 = False

    try:
        if W.shape[1] == 0:
            h3 = True
        else:
            TW = T * W
            W_TW = W.row_join(TW)
            h3 = W.rank() == W_TW.rank()
    except Exception:
        h3 = False

    try:
        n = T.shape[0]
        T_W = T.row_join(-W)
        null_basis = T_W.nullspace()
        if not null_basis:
            h4 = True
        else:
            N = T_W.__class__.hstack(*null_basis)
            X = N[:n, :]
            W_X = W.row_join(X)
            h4 = W.rank() == W_X.rank()
    except Exception:
        h4 = False

    try:
        n = T.shape[0]
        neg_q = T.rank() < n
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: V is a vector space over a field F",
    "H_2: T is a linear operator on V",
    "H_3: W is a T-invariant subspace of V",
    "H_4: The induced quotient operator T/W on the quotient space V/W is injective",
    "¬Q: T is not injective"
]

N_HYP = 4
NEG_Q_INDEX = 4