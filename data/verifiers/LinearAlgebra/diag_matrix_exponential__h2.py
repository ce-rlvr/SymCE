import sympy
from sympy.matrices import MatrixBase
from sympy import eye, zeros, I, pi, Matrix

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        h1 = isinstance(witness, MatrixBase) and witness.is_square
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            exp_A = witness.exp()
            diag = exp_A.is_diagonalizable()
            neg_q = (diag is False)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    r"H_1: A is an n \times n matrix over the complex numbers",
    r"¬Q: The matrix exponential e^A is not diagonalizable"
]

N_HYP = 1
NEG_Q_INDEX = 1