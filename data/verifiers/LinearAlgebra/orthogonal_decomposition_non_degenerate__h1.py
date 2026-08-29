import sympy
from sympy import Matrix, eye, zeros

# Top-level setup: named object bindings that the witness expression may reference.
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    Returns a list of booleans: [H_1_ok, H_2_ok, neg_Q_ok]
    """
    try:
        if callable(witness):
            witness = witness()
    except Exception:
        pass

    # 1. Try duck-typing / dictionary for custom objects (e.g., infinite-dimensional spaces)
    try:
        if hasattr(witness, '__dict__') or isinstance(witness, dict):
            def get_val(names, default):
                if isinstance(witness, dict):
                    for n in names:
                        if n in witness:
                            v = witness[n]
                            return v() if callable(v) else v
                else:
                    for n in names:
                        if hasattr(witness, n):
                            v = getattr(witness, n)
                            return v() if callable(v) else v
                return default

            h1_val = get_val(['B_is_symmetric', 'is_symmetric', 'h1'], None)
            h2_val = get_val(['W_is_non_degenerate', 'is_non_degenerate', 'h2'], None)
            q_val = get_val(['is_direct_sum', 'q'], None)
            neg_q_val = get_val(['neg_q', 'is_not_direct_sum'], None)

            if neg_q_val is None and q_val is not None:
                neg_q_val = not q_val

            if h1_val is not None and h2_val is not None and neg_q_val is not None:
                return [bool(h1_val), bool(h2_val), bool(neg_q_val)]
    except Exception:
        pass

    # 2. Try tuple/list of matrices (B, W) or (V, B, W) for finite-dimensional modules over rings
    try:
        if isinstance(witness, (tuple, list)) and len(witness) in (2, 3):
            B, W = witness[-2], witness[-1]
            
            if isinstance(B, (list, tuple)):
                B = Matrix(B)
            if isinstance(W, (list, tuple)):
                W = Matrix(W)
                
            if hasattr(B, 'is_square') and hasattr(W, 'rows'):
                # H1: B is a symmetric bilinear form
                h1 = bool(B.is_square and B == B.T)
                
                # H2: Restriction of B to W is non-degenerate
                B_W = W.T * B * W
                h2 = bool(B_W.det() != 0)
                
                # neg_Q: V is not the internal direct sum of W and W^\perp
                null_basis = (W.T * B).nullspace()
                if not null_basis:
                    U = Matrix(B.rows, 0, [])
                else:
                    U = Matrix.hstack(*null_basis)
                    
                M = Matrix.hstack(W, U)
                if M.rows != M.cols:
                    neg_q = True
                else:
                    try:
                        M_inv = M.inv()
                        def is_int(val):
                            if isinstance(val, int):
                                return True
                            return getattr(val, 'is_integer', False)
                        
                        # If M is not invertible over Z, it's not a direct sum of free modules
                        if any(not is_int(x) for x in M_inv):
                            neg_q = True
                        else:
                            neg_q = False
                    except Exception:
                        neg_q = True
                        
                return [h1, h2, neg_q]
    except Exception:
        pass

    return [False, False, False]

CONDITION_LABELS = [
    "H_1: B is a symmetric bilinear form on V",
    "H_2: W is a subspace of V such that the restriction of B to W is non-degenerate",
    "¬Q: V is not the internal direct sum of W and the orthogonal complement of W"
]

N_HYP = 2
NEG_Q_INDEX = 2