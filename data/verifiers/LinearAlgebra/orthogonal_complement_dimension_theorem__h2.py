import sympy
from sympy import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        # Parse witness
        if isinstance(witness, tuple):
            if len(witness) == 2:
                W_raw, B_raw = witness
            elif len(witness) == 3:
                _, W_raw, B_raw = witness
            else:
                return [False, False, False, False]
        elif isinstance(witness, dict):
            W_raw = witness.get('W')
            B_raw = witness.get('B')
        else:
            return [False, False, False, False]
            
        B = Matrix(B_raw)
        
        # Robustly parse W into a matrix where rows span the subspace
        if isinstance(W_raw, list):
            if len(W_raw) == 0:
                W = zeros(0, B.cols)
            elif all(isinstance(w, Matrix) for w in W_raw):
                rows = [w.T if w.cols == 1 else w for w in W_raw]
                W = sympy.Matrix.vstack(*rows)
            else:
                W = Matrix(W_raw)
        else:
            W = Matrix(W_raw)
            
    except Exception:
        return [False, False, False, False]

    # H1: V is a finite-dimensional vector space over a field F
    try:
        h1_ok = bool(B.is_square)
    except Exception:
        h1_ok = False

    # H2: W is a subspace of V
    try:
        h2_ok = bool(W.cols == B.cols)
    except Exception:
        h2_ok = False

    # H3: W^\perp is the orthogonal complement of W with respect to B
    # This is definitional in our check, so it holds if the objects are valid.
    try:
        h3_ok = h1_ok and h2_ok
    except Exception:
        h3_ok = False

    # neg_Q: \dim(W) + \dim(W^\perp) \neq \dim(V)
    try:
        if h1_ok and h2_ok:
            n = B.cols
            dim_W = W.rank()
            
            # W^\perp = {x \in V | w^T B x = 0 for all w \in W}
            # This is exactly the nullspace of the matrix product (W * B)
            dim_W_perp = n - (W * B).rank()
            
            neg_Q_ok = bool((dim_W + dim_W_perp) != n)
        else:
            neg_Q_ok = False
    except Exception:
        neg_Q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_Q_ok]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over a field F",
    "H_2: W is a subspace of V",
    "H_3: W^\\perp is the orthogonal complement of W with respect to B",
    "¬Q: \\dim(W) + \\dim(W^\\perp) \\neq \\dim(V)"
]

N_HYP = 3
NEG_Q_INDEX = 3