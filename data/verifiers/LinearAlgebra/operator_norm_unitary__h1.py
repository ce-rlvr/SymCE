import sympy
from sympy import eye, zeros, Matrix

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if not getattr(witness, 'is_Matrix', False):
            h1 = False
        elif not witness.is_square:
            h1 = False
        else:
            n = witness.shape[0]
            diff = sympy.simplify(witness.H * witness - eye(n))
            h1 = bool(diff == zeros(n, n))
    except Exception:
        h1 = False

    try:
        if not getattr(witness, 'is_Matrix', False):
            neg_q = False
        elif witness.shape[0] == 0 or witness.shape[1] == 0:
            # The 2-norm of an empty matrix is 0, which is not 1.
            neg_q = True
        else:
            norm2 = witness.norm(2)
            neg_q = bool(sympy.simplify(norm2 - 1) != 0)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: U is a unitary matrix",
    "¬Q: The induced operator 2-norm of U is not exactly 1"
]

N_HYP = 1
NEG_Q_INDEX = 1