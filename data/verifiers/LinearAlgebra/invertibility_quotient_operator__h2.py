import sympy
from sympy import Matrix, zeros, eye
from sympy.abc import x, y, z

# Common linear algebra objects for potential use in witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the given witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (T, W) where:
      - T is a sympy Matrix representing a linear operator on V = R^n.
      - W is a sympy Matrix whose columns span the subspace W, 
        OR a list of sympy Matrices representing the basis vectors of W.
    """
    # H_1: V is a finite-dimensional vector space and W is a subspace
    try:
        T, W = witness
        if not isinstance(T, Matrix) or not T.is_square:
            h1 = False
        else:
            n = T.shape[0]
            if isinstance(W, Matrix):
                W_mat = W
                h1 = (W_mat.shape[0] == n)
            elif isinstance(W, (list, tuple)):
                if len(W) == 0:
                    W_mat = zeros(n, 1)
                    h1 = True
                else:
                    try:
                        cols = []
                        for w in W:
                            w_mat = w if isinstance(w, Matrix) else Matrix(w)
                            # If given as a row vector, transpose to column vector
                            if w_mat.shape[0] == 1 and w_mat.shape[1] == n:
                                w_mat = w_mat.T
                            cols.append(w_mat)
                        W_mat = Matrix.hstack(*cols)
                        h1 = (W_mat.shape[0] == n)
                    except Exception:
                        h1 = False
            else:
                h1 = False
    except Exception:
        h1 = False

    # H_2: W is invariant under T
    try:
        if h1:
            # W is invariant under T iff the column space of T*W is contained in the column space of W.
            # This is equivalent to rank([W, T*W]) == rank(W).
            TW = T * W_mat
            W_TW = Matrix.hstack(W_mat, TW)
            h2 = (W_TW.rank() == W_mat.rank())
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: The quotient operator T/W is NOT invertible
    try:
        if h1:
            # T/W is an operator on V/W. It is invertible iff it is surjective.
            # Im(T/W) = (Im(T) + W) / W.
            # T/W is surjective iff dim(Im(T) + W) = n.
            # The subspace Im(T) + W is spanned by the columns of T and the columns of W.
            # Therefore, T/W is invertible iff rank([T, W]) == n.
            # The conclusion FAILS (T/W is NOT invertible) iff rank([T, W]) < n.
            T_W = Matrix.hstack(T, W_mat)
            neg_q = (T_W.rank() < n)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space and W is a subspace",
    "H_2: W is invariant under T",
    "¬Q: The quotient operator T/W is not invertible"
]

N_HYP = 2
NEG_Q_INDEX = 2