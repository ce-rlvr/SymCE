import sympy
from sympy import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if not getattr(witness, 'is_square', False):
            return [False, False, False]
        n = witness.shape[0]
        I = eye(n)
    except Exception:
        return [False, False, False]

    try:
        h1 = bool(witness.T * witness == I and witness * witness.T == I)
    except Exception:
        h1 = False

    try:
        h2 = bool(witness == witness.T)
    except Exception:
        h2 = False

    try:
        neg_q = bool(witness * witness != I)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: Q is an orthogonal matrix",
    "H_2: Q is a symmetric matrix",
    "¬Q: Q is not an involution (Q^2 != I)"
]

N_HYP = 2
NEG_Q_INDEX = 2