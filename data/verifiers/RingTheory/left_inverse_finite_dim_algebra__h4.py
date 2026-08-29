import sympy
from sympy import eye, zeros, MatrixBase, Expr

# Top-level setup: named object bindings that the witness expression may reference.
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: witness is a tuple (x, y)
    try:
        h1 = isinstance(witness, (tuple, list)) and len(witness) == 2
    except Exception:
        h1 = False

    # H_2: x and y are elements of a finite-dimensional algebra (matrices of same size or scalars)
    try:
        if h1:
            x, y = witness
            if isinstance(x, MatrixBase) and isinstance(y, MatrixBase):
                h2 = x.is_square and y.is_square and x.shape == y.shape
            else:
                h2 = isinstance(x, (int, float, Expr)) and isinstance(y, (int, float, Expr))
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: x is not a unit with y as its unique two-sided inverse
    try:
        if h2:
            x, y = witness
            if isinstance(x, MatrixBase):
                n = x.shape[0]
                I = eye(n)
                q = (x * y == I) and (y * x == I)
            else:
                q = (x * y == 1) and (y * x == 1)
            neg_q = not q
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: witness is a tuple (x, y)",
    "H_2: x and y are elements of a finite-dimensional algebra (matrices of same size or scalars)",
    "¬Q: x is not a unit with y as its unique two-sided inverse"
]

N_HYP = 2
NEG_Q_INDEX = 2