import sympy
from sympy import eye, zeros, Matrix

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        # Check if U is a unitary matrix (or isometry if not square)
        # U^H * U == I or U * U^H == I
        cond1 = (witness.H * witness).expand() == eye(witness.cols)
        cond2 = (witness * witness.H).expand() == eye(witness.rows)
        h1 = bool(cond1 or cond2)
    except Exception:
        h1 = False

    try:
        # Check if U is invertible and its inverse is unitary
        if not getattr(witness, 'is_square', False):
            q = False
        else:
            inv_U = witness.inv()
            q = bool((inv_U.H * inv_U).expand() == eye(inv_U.cols))
        neg_q = not q
    except Exception:
        # If inversion fails (e.g., singular matrix), it is not invertible
        neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: U is a unitary matrix",
    "¬Q: U is not invertible or its inverse is not unitary"
]

N_HYP = 1
NEG_Q_INDEX = 1