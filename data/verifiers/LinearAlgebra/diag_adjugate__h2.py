import sympy
from sympy import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        h1 = isinstance(witness, sympy.matrices.MatrixBase) and witness.is_square
    except Exception:
        h1 = False

    try:
        adj = witness.adjugate()
        neg_q = not adj.is_diagonalizable()
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: A is a square matrix",
    "¬Q: The adjugate matrix of A is not diagonalizable"
]

N_HYP = 1
NEG_Q_INDEX = 1