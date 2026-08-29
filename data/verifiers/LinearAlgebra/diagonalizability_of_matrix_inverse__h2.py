import sympy
from sympy.matrices import MatrixBase, eye, zeros
from sympy import Matrix

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
        if isinstance(witness, MatrixBase) and witness.is_square:
            h2 = bool(witness.is_diagonalizable())
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        if isinstance(witness, MatrixBase) and witness.is_square:
            if witness.det() == 0:
                neg_q = True
            else:
                neg_q = not bool(witness.inv().is_diagonalizable())
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is a square matrix",
    "H_2: A is diagonalizable",
    "¬Q: A^{-1} is not diagonalizable or does not exist"
]

N_HYP = 2
NEG_Q_INDEX = 2