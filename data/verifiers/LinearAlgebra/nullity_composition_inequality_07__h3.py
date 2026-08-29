import sympy as sp

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            U = witness.get('U')
            V = witness.get('V')
            W = witness.get('W')
            S = witness.get('S')
            T = witness.get('T')
        elif isinstance(witness, tuple):
            if len(witness) == 5:
                U, V, W, S, T = witness
            elif len(witness) == 2:
                S, T = witness
                U = T.cols if hasattr(T, 'cols') else None
                V = T.rows if hasattr(T, 'rows') else None
                W = S.rows if hasattr(S, 'rows') else None
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: U, V, and W are finite-dimensional vector spaces over a field F
    try:
        if hasattr(U, 'dimension'):
            dim_U = U.dimension
        elif hasattr(U, 'shape'):
            dim_U = U.shape[0] * U.shape[1]
        else:
            dim_U = int(U)
            
        if hasattr(V, 'dimension'):
            dim_V = V.dimension
        elif hasattr(V, 'shape'):
            dim_V = V.shape[0] * V.shape[1]
        else:
            dim_V = int(V)
            
        if hasattr(W, 'dimension'):
            dim_W = W.dimension
        elif hasattr(W, 'shape'):
            dim_W = W.shape[0] * W.shape[1]
        else:
            dim_W = int(W)
            
        h1 = dim_U >= 0 and dim_V >= 0 and dim_W >= 0
    except Exception:
        h1 = False

    # H2: T: U -> V is a linear transformation
    try:
        h2 = isinstance(T, sp.MatrixBase) and T.rows == dim_V and T.cols == dim_U
    except Exception:
        h2 = False

    # neg_Q: nullity(S \circ T) <= nullity(S) + nullity(T) must FAIL
    try:
        if isinstance(S, sp.MatrixBase) and isinstance(T, sp.MatrixBase):
            if S.cols != T.rows:
                # If dimensions do not match, the composition is undefined, so the conclusion fails
                neg_q = True
            else:
                ST = S * T
                nullity_ST = ST.cols - ST.rank()
                nullity_S = S.cols - S.rank()
                nullity_T = T.cols - T.rank()
                q = nullity_ST <= nullity_S + nullity_T
                neg_q = not q
        elif callable(S):
            # If S is a non-linear function, nullity is undefined, so the conclusion fails
            neg_q = True
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: U, V, and W are finite-dimensional vector spaces over a field F",
    "H_2: T: U -> V is a linear transformation",
    "¬Q: nullity(S \circ T) > nullity(S) + nullity(T) or composition is undefined"
]

N_HYP = 2
NEG_Q_INDEX = 2