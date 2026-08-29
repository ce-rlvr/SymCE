import sympy as sp
from sympy import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Given a witness tuple (T, S, U), where T and S are matrices representing 
    linear operators on V, and U is a matrix whose columns span a subspace of V.
    """
    try:
        T, S, U = witness
    except Exception:
        return [False, False, False, False]

    # Normalize T
    try:
        if not isinstance(T, sp.MatrixBase):
            T = sp.Matrix(T)
    except Exception:
        pass

    # Normalize S
    try:
        if not isinstance(S, sp.MatrixBase):
            S = sp.Matrix(S)
    except Exception:
        pass

    # Normalize U
    try:
        if isinstance(U, list) and len(U) > 0 and isinstance(U[0], sp.MatrixBase):
            U = sp.Matrix.hstack(*U)
        elif not isinstance(U, sp.MatrixBase):
            U = sp.Matrix(U)
    except Exception:
        pass

    # H_1: T and S are linear operators on V
    try:
        h1 = bool(T.is_square and S.is_square and T.shape == S.shape and U.rows == T.rows)
    except Exception:
        h1 = False

    # H_2: S is an invertible operator
    try:
        h2 = bool(S.det() != 0)
    except Exception:
        h2 = False

    # H_3: U is a T-invariant subspace of V
    try:
        if U.cols == 0:
            h3 = True
        else:
            # U is T-invariant if T(U) is contained in the span of U
            h3 = bool(U.rank() == U.row_join(T * U).rank())
    except Exception:
        h3 = False

    # ¬Q: The image subspace S(U) is NOT invariant under the operator S T S^{-1}
    try:
        if U.cols == 0:
            neg_q = False
        else:
            M = S * T * S.inv()
            SU = S * U
            # S(U) is invariant under M if M(S(U)) is contained in the span of S(U)
            neg_q = bool(SU.rank() != SU.row_join(M * SU).rank())
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: T and S are linear operators on V",
    "H_2: S is an invertible operator",
    "H_3: U is a T-invariant subspace of V",
    "¬Q: S(U) is not invariant under S T S^{-1}"
]

N_HYP = 3
NEG_Q_INDEX = 3