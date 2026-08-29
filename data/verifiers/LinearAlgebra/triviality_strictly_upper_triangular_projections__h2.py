import sympy
from sympy import eye, zeros
from sympy.matrices import MatrixBase

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        h1 = isinstance(witness, MatrixBase) and witness.rows == witness.cols and witness.rows > 0
    except Exception:
        h1 = False

    try:
        h2 = bool(witness**2 == witness)
    except Exception:
        h2 = False

    try:
        neg_q = bool(witness != zeros(witness.rows, witness.cols))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: P is an n x n matrix",
    "H_2: P is a projection matrix (P^2 = P)",
    "¬Q: P is not the n x n zero matrix"
]

N_HYP = 2
NEG_Q_INDEX = 2