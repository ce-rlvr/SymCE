import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        h1 = isinstance(witness, sympy.MatrixBase) and witness.is_square
    except Exception:
        h1 = False

    try:
        # Standard sympy matrices are over fields of characteristic 0 (e.g., Reals, Rationals)
        h2 = isinstance(witness, sympy.MatrixBase)
    except Exception:
        h2 = False

    try:
        neg_q = (witness.rank() % 2 != 0)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix",
    "H_2: The underlying field has characteristic not equal to 2",
    "¬Q: The rank of A is not an even integer"
]

N_HYP = 2
NEG_Q_INDEX = 2