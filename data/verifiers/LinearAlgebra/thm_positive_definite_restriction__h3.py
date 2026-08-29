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

    try:
        if isinstance(W, (list, tuple)):
            if len(W) == 0:
                W = zeros(T.rows, 0)
            elif isinstance(W[0], Matrix):
                W = Matrix.hstack(*W)
            else:
                W = Matrix(W)
    except Exception:
        pass

    # H_1: V is a finite-dimensional inner product space
    try:
        h1 = isinstance(T, Matrix) and isinstance(W, Matrix) and T.is_square and T.rows == W.rows
    except Exception:
        h1 = False

    # H_2: T is a positive definite self-adjoint operator on V
    try:
        if not h1:
            h2 = False
        else:
            is_self_adjoint = (T == T.H)
            if not is_self_adjoint:
                h2 = False
            else:
                h2 = True
                for i in range(1, T.rows + 1):
                    minor_det = T[:i, :i].det()
                    try:
                        val = float(minor_det)
                        if val <= 0:
                            h2 = False
                            break
                    except TypeError:
                        try:
                            if bool(sympy.re(minor_det) <= 0):
                                h2 = False
                                break
                        except TypeError:
                            h2 = False
                            break
    except Exception:
        h2 = False

    # neg_Q: The restriction operator T|_W is not a positive definite self-adjoint operator on W
    # (This happens if and only if W is not T-invariant, meaning T|_W is not an operator on W)
    try:
        if not h1:
            neg_q = False
        else:
            rank_W = W.rank()
            rank_WTW = W.row_join(T * W).rank()
            is_invariant = (rank_WTW == rank_W)
            neg_q = not is_invariant
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional inner product space",
    "H_2: T is a positive definite self-adjoint operator on V",
    "¬Q: The restriction operator T|_W is not a positive definite self-adjoint operator on W"
]

N_HYP = 2
NEG_Q_INDEX = 2