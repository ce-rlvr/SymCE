import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if not isinstance(witness, sympy.MatrixBase):
            h1 = False
        elif not witness.is_square:
            h1 = False
        else:
            h1 = all(entry.is_real for entry in witness)
    except Exception:
        h1 = False

    try:
        h2 = bool(witness == witness.T)
    except Exception:
        h2 = False

    try:
        det_A = witness.det()
        neg_q = bool(det_A <= 0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix with real entries",
    "H_2: A is symmetric",
    "¬Q: The determinant of A is less than or equal to zero"
]

N_HYP = 2
NEG_Q_INDEX = 2