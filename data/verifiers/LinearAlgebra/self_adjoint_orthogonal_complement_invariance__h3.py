import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        T, W = witness
    except Exception:
        return [False, False, False]
        
    # H1: V is an inner product space (valid dimensions)
    h1_ok = False
    try:
        if isinstance(T, Matrix) and T.is_square:
            n = T.shape[0]
            if isinstance(W, list):
                h1_ok = True
                for w in W:
                    if not isinstance(w, Matrix) or w.shape != (n, 1):
                        h1_ok = False
                        break
            elif isinstance(W, Matrix):
                h1_ok = W.shape[0] == n
            else:
                h1_ok = False
    except Exception:
        h1_ok = False

    # H2: T is self-adjoint
    h2_ok = False
    try:
        if h1_ok:
            diff = (T - T.H).expand()
            h2_ok = all(sympy.simplify(val) == 0 for val in diff)
    except Exception:
        h2_ok = False

    # neg_Q: W^\perp is NOT T-invariant
    neg_q_ok = False
    try:
        if h1_ok:
            n = T.shape[0]
            if isinstance(W, list):
                if len(W) == 0:
                    W_mat = zeros(n, 1)
                else:
                    W_mat = Matrix.hstack(*W)
            else:
                W_mat = W
                
            W_perp = W_mat.H.nullspace()
            is_invariant = True
            for v in W_perp:
                Tv = T * v
                prod = W_mat.H * Tv
                for val in prod:
                    if sympy.simplify(val) != 0:
                        is_invariant = False
                        break
                if not is_invariant:
                    break
            neg_q_ok = not is_invariant
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: V is an inner product space",
    "H_2: T: V \\to V is a self-adjoint linear operator",
    "¬Q: The orthogonal complement W^\\perp is not a T-invariant subspace of V"
]

N_HYP = 2
NEG_Q_INDEX = 2