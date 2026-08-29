import sympy
from sympy import Matrix, eye, zeros, I, Rational, Integer
from sympy.abc import x, y, z

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        # Check if witness is a square matrix over the complex numbers (no free symbols)
        h1 = bool(isinstance(witness, Matrix) and witness.is_square and len(witness.free_symbols) == 0)
    except Exception:
        h1 = False

    try:
        # Check if the matrix is NOT diagonalizable
        diag = witness.is_diagonalizable()
        neg_q = bool(diag is False)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: The underlying field is the field of complex numbers",
    "¬Q: P is not diagonalizable"
]

N_HYP = 1
NEG_Q_INDEX = 1