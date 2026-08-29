import sympy
from sympy import Matrix, zeros, eye

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness satisfies the hypotheses and the negated conclusion.
    The witness should be a tuple (T, W), where T is an n x n matrix representing 
    the linear operator, and W is a list of n-dimensional vectors (or an n x k matrix) 
    representing the subspace.
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        T, W = witness
    except Exception:
        return [False, False, False]

    # H_1: V is a vector space over a field F
    # (Implicitly verified by checking if T is a square matrix and W contains vectors of matching dimension)
    h1_ok = False
    try:
        T_mat = Matrix(T)
        if T_mat.is_square:
            n = T_mat.shape[0]
            if isinstance(W, (list, tuple)):
                if len(W) == 0:
                    M_W = zeros(n, 1)
                    h1_ok = True
                else:
                    W_mats = []
                    for w in W:
                        w_mat = Matrix(w)
                        if w_mat.shape == (n, 1):
                            W_mats.append(w_mat)
                        elif w_mat.shape == (1, n):
                            W_mats.append(w_mat.T)
                        else:
                            raise ValueError("Vector dimensions do not match the space V")
                    M_W = Matrix.hstack(*W_mats)
                    h1_ok = True
            else:
                W_mat = Matrix(W)
                if W_mat.shape[0] == n:
                    if W_mat.shape[1] == 0:
                        M_W = zeros(n, 1)
                    else:
                        M_W = W_mat
                    h1_ok = True
    except Exception:
        h1_ok = False

    # H_2: W is a T-invariant subspace of V
    h2_ok = False
    try:
        if h1_ok:
            rank_W = M_W.rank()
            is_invariant = True
            for i in range(M_W.shape[1]):
                w = M_W[:, i]
                Tw = T_mat * w
                # If adding Tw to the generators of W increases the rank, Tw is not in W
                if M_W.row_join(Tw).rank() > rank_W:
                    is_invariant = False
                    break
            h2_ok = is_invariant
    except Exception:
        h2_ok = False

    # ¬Q: The induced quotient operator T/W on the quotient space V/W is not surjective
    # T/W is surjective iff Im(T) + W = V. Thus, it is NOT surjective iff rank([T, W]) < n.
    neg_q_ok = False
    try:
        if h1_ok:
            rank_TW = T_mat.row_join(M_W).rank()
            neg_q_ok = bool(rank_TW < n)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: V is a vector space over a field F",
    "H_2: W is a T-invariant subspace of V",
    "¬Q: The induced quotient operator T/W on the quotient space V/W is not surjective"
]

N_HYP = 2
NEG_Q_INDEX = 2