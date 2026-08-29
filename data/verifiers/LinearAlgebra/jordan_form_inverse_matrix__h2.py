import sympy
from sympy import Matrix, eye, zeros, MatrixBase

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        h1 = bool(isinstance(witness, MatrixBase) and witness.is_square)
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            det_val = witness.det()
            if det_val == 0:
                neg_q = True
            elif sympy.simplify(det_val) == 0:
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix over an algebraically closed field F",
    "¬Q: The conclusion about the Jordan form of A^{-1} fails"
]

N_HYP = 1
NEG_Q_INDEX = 1