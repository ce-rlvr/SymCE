import sympy
from sympy import I, eye, zeros, Matrix, MatrixBase
import math

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, MatrixBase):
            U = Matrix(witness)
        else:
            U = witness
        h1 = bool(U.is_square and all(e.is_number for e in U))
    except Exception:
        h1 = False

    try:
        if not isinstance(witness, MatrixBase):
            U = Matrix(witness)
        else:
            U = witness
        det_U = U.det()
        abs_det = sympy.Abs(det_U)
        diff = abs_det - 1
        val = complex(diff.evalf())
        neg_q = bool(abs(val) > 1e-12)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: U is an n x n complex matrix",
    "¬Q: The determinant of U does not have an absolute value of 1"
]

N_HYP = 1
NEG_Q_INDEX = 1