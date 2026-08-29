import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (T, W), where:
      - T is a sympy.Matrix representing the linear operator.
      - W is either a list of sympy.Matrix column vectors or a single sympy.Matrix 
        whose columns span the subspace W.
    """
    try:
        T, W = witness
    except Exception:
        return [False, False, False]

    # H_1: V is a finite-dimensional vector space
    try:
        h1 = isinstance(T, Matrix) and T.is_square
        if h1:
            n = T.shape[0]
            if isinstance(W, list):
                h1 = all(isinstance(w, Matrix) and w.shape == (n, 1) for w in W)
            elif isinstance(W, Matrix):
                h1 = W.shape[0] == n
            else:
                h1 = False
    except Exception:
        h1 = False

    # H_2: T is an invertible linear operator
    try:
        h2 = False
        if h1:
            h2 = (T.det() != 0)
    except Exception:
        h2 = False

    # ¬Q: W is not invariant under T^{-1}
    try:
        neg_q = False
        if h2:
            T_inv = T.inv()
            if isinstance(W, list):
                if len(W) == 0:
                    W_mat = zeros(T.shape[0], 0)
                else:
                    W_mat = W[0]
                    for w in W[1:]:
                        W_mat = W_mat.row_join(w)
            else:
                W_mat = W
            
            if W_mat.shape[1] == 0:
                neg_q = False
            else:
                rank_W = W_mat.rank()
                augmented = W_mat.row_join(T_inv * W_mat)
                neg_q = augmented.rank() > rank_W
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space",
    "H_2: T is an invertible linear operator",
    "¬Q: W is not invariant under T^{-1}"
]

N_HYP = 2
NEG_Q_INDEX = 2