import sympy
from sympy.matrices import MatrixBase, eye, zeros
from sympy import abc

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        h1 = isinstance(witness, MatrixBase) and witness.is_square
    except Exception:
        h1 = False

    try:
        det_val = sympy.simplify(witness.det())
        neg_q = bool(det_val == 0)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is a square matrix",
    "¬Q: The formula det(A)tr(A^{-1}H) is undefined (A is not invertible)"
]

N_HYP = 1
NEG_Q_INDEX = 1