import sympy
from sympy import Matrix, zeros, eye

# Top-level setup: named object bindings that the witness expression may reference
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def _is_zero(expr):
    if expr == 0:
        return True
    if hasattr(expr, 'is_zero') and expr.is_zero is True:
        return True
    try:
        return sympy.simplify(expr) == 0
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        T, W = witness
    except Exception:
        return [False, False, False, False, False]

    # H_1: T is a square matrix representing a linear operator on V
    try:
        h1 = isinstance(T, sympy.MatrixBase) and T.is_square
    except Exception:
        h1 = False

    # H_2: W represents a subspace of V (matrix whose columns span W)
    try:
        if isinstance(W, (list, tuple)):
            if len(W) == 0:
                W_mat = zeros(T.rows, 0)
            elif all(isinstance(c, sympy.MatrixBase) for c in W):
                W_mat = sympy.Matrix.hstack(*W)
            else:
                W_mat = sympy.Matrix(W)
        else:
            W_mat = W
        h2 = isinstance(W_mat, sympy.MatrixBase) and W_mat.rows == T.rows
    except Exception:
        h2 = False

    # H_3: W is T-invariant
    try:
        TW = T * W_mat
        aug = W_mat.row_join(TW)
        h3 = W_mat.rank() == aug.rank()
    except Exception:
        h3 = False

    # H_4: T|_W is nilpotent
    try:
        n = T.rows
        TnW = (T**n) * W_mat
        h4 = all(_is_zero(e) for e in TnW)
    except Exception:
        h4 = False

    # ¬Q: T is not nilpotent
    try:
        n = T.rows
        Tn = T**n
        neg_q = not all(_is_zero(e) for e in Tn)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: T is a square matrix representing a linear operator on V",
    "H_2: W represents a subspace of V",
    "H_3: W is T-invariant",
    "H_4: T|_W is nilpotent",
    "¬Q: T is not nilpotent"
]

N_HYP = 4
NEG_Q_INDEX = 4