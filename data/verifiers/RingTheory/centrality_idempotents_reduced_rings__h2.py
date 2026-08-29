import sympy
from sympy import Matrix, eye, zeros, simplify
from sympy.matrices.matrixbase import MatrixBase
from sympy.core.expr import Expr

# Standard matrix rings for counterexamples
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                R, e, x = witness
            elif len(witness) == 2:
                e, x = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: R is a ring
    try:
        # Check if e and x can be added and multiplied (basic ring operations)
        _ = e + x
        _ = e * x
        _ = x * e
        _ = e * e
        
        if isinstance(e, MatrixBase) and isinstance(x, MatrixBase):
            # For matrices, they must be square and of the same dimension to form a ring
            h1 = (e.shape == x.shape) and (e.shape[0] == e.shape[1])
        else:
            # For other types (scalars, expressions), if operations succeed, we assume they belong to a ring
            h1 = True
    except Exception:
        h1 = False

    # H_2: e is an idempotent element of R
    try:
        if isinstance(e, MatrixBase):
            h2 = bool(e * e == e)
        else:
            h2 = bool(simplify(e * e - e) == 0)
    except Exception:
        h2 = False

    # H_3: x is an element of R
    try:
        # If H_1 holds, x is compatible with e and thus in the same ring
        h3 = h1
    except Exception:
        h3 = False

    # ¬Q: ex != xe (e is not in the center of R)
    try:
        if isinstance(e, MatrixBase) and isinstance(x, MatrixBase):
            neg_q = bool(e * x != x * e)
        else:
            neg_q = bool(simplify(e * x - x * e) != 0)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: e is an idempotent element of R",
    "H_3: x is an element of R",
    "¬Q: ex != xe"
]

N_HYP = 3
NEG_Q_INDEX = 3