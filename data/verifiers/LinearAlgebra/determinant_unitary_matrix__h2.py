import sympy
from sympy import eye, zeros, Matrix, ImmutableMatrix, I, Abs, simplify
from sympy.matrices import MatrixBase

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        h1 = bool(isinstance(witness, MatrixBase) and witness.is_square)
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            d = witness.det()
            modulus = simplify(Abs(d))
            neg_q = bool(modulus != 1)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: U is an n x n complex matrix",
    "¬Q: The determinant of U does not have a modulus of exactly 1"
]

N_HYP = 1
NEG_Q_INDEX = 1