import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        h1 = False
        if hasattr(witness, 'is_Matrix') and witness.is_Matrix:
            if witness.T * witness == eye(witness.cols):
                h1 = True
            elif witness * witness.T == eye(witness.rows):
                h1 = True
    except Exception:
        h1 = False

    try:
        neg_q = False
        if hasattr(witness, 'is_Matrix') and witness.is_Matrix:
            if witness.rows != witness.cols:
                neg_q = True
            else:
                if witness * witness.T != witness.T * witness:
                    neg_q = True
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: Q is an orthogonal matrix",
    "¬Q: Q is not a normal matrix (Q Q^T != Q^T Q)"
]

N_HYP = 1
NEG_Q_INDEX = 1