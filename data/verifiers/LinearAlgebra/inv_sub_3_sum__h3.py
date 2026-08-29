import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_basis(S, n):
    """
    Helper function to extract a basis (list of column vectors) from a subspace representation.
    S can be a sympy Matrix (columns span the subspace) or a list/tuple of vectors.
    n is the dimension of the vector space V.
    """
    if isinstance(S, Matrix):
        if S.rows != n:
            return None
        return S.columnspace()
    elif isinstance(S, (list, tuple)):
        if len(S) == 0:
            return []
        S_mats = []
        for v in S:
            try:
                v_mat = Matrix(v)
            except Exception:
                return None
            # If given as a row vector, transpose it to a column vector
            if v_mat.rows == 1 and v_mat.cols == n:
                v_mat = v_mat.T
            if v_mat.rows != n or v_mat.cols != 1:
                return None
            S_mats.append(v_mat)
        M = Matrix.hstack(*S_mats)
        return M.columnspace()
    return None

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the false conjecture.
    The witness is expected to be a tuple (T, U, W) where:
      - T is a sympy Matrix representing a linear operator on V = R^n.
      - U is a representation of a subspace (Matrix or list of vectors).
      - W is a representation of a subspace (Matrix or list of vectors).
    """
    try:
        T, U, W = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: V is a vector space
    # Implicitly true if T is a square matrix and U, W are valid subspace representations in V.
    try:
        h1 = isinstance(T, Matrix) and T.is_square
        if h1:
            n = T.rows
            U_basis = get_basis(U, n)
            W_basis = get_basis(W, n)
            if U_basis is None or W_basis is None:
                h1 = False
    except Exception:
        h1 = False

    # H_2: T is a linear operator on V
    try:
        h2 = isinstance(T, Matrix) and T.is_square
    except Exception:
        h2 = False

    # H_3: W is a T-invariant subspace of V
    try:
        n = T.rows
        W_basis = get_basis(W, n)
        if W_basis is None:
            h3 = False
        elif len(W_basis) == 0:
            h3 = True  # The zero subspace is always invariant
        else:
            W_mat = Matrix.hstack(*W_basis)
            rank_W = W_mat.rank()
            h3 = True
            for v in W_basis:
                Tv = T * v
                if Matrix.hstack(W_mat, Tv).rank() > rank_W:
                    h3 = False
                    break
    except Exception:
        h3 = False

    # ¬Q: The sum U + W is NOT a T-invariant subspace of V
    try:
        n = T.rows
        U_basis = get_basis(U, n)
        W_basis = get_basis(W, n)
        if U_basis is None or W_basis is None:
            neg_q = False
        else:
            UW_basis = U_basis + W_basis
            if len(UW_basis) == 0:
                neg_q = False  # The zero subspace is invariant, so ¬Q is False
            else:
                UW_mat = Matrix.hstack(*UW_basis)
                rank_UW = UW_mat.rank()
                neg_q = False
                for v in UW_basis:
                    Tv = T * v
                    if Matrix.hstack(UW_mat, Tv).rank() > rank_UW:
                        neg_q = True
                        break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: V is a vector space",
    "H_2: T is a linear operator on V",
    "H_3: W is a T-invariant subspace of V",
    "¬Q: The sum U + W is not a T-invariant subspace of V"
]

N_HYP = 3
NEG_Q_INDEX = 3