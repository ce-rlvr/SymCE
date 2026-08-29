import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if not getattr(witness, 'is_Matrix', False):
            h1 = False
        else:
            diff = witness.T * witness - eye(witness.cols)
            h1 = all(sympy.simplify(e) == 0 for e in diff)
    except Exception:
        h1 = False

    try:
        if not getattr(witness, 'is_Matrix', False):
            neg_q = False
        else:
            diff2 = witness * witness.T - eye(witness.rows)
            neg_q = not all(sympy.simplify(e) == 0 for e in diff2)
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: Q is an orthogonal matrix",
    "¬Q: Q^T is not an orthogonal matrix"
]

N_HYP = 1
NEG_Q_INDEX = 1