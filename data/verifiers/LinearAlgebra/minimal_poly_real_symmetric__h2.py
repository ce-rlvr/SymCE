import sympy
from sympy import MatrixBase, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H_1: A is an n x n matrix with real entries
    try:
        if not isinstance(witness, MatrixBase):
            h1 = False
        elif not witness.is_square:
            h1 = False
        else:
            h1 = all(e.is_real == True for e in witness)
    except Exception:
        h1 = False

    # neg_Q: The minimal polynomial of A has repeated roots
    # A matrix has a minimal polynomial with repeated roots iff it is NOT diagonalizable over C.
    try:
        if not isinstance(witness, MatrixBase) or not witness.is_square:
            neg_q = False
        else:
            neg_q = not witness.is_diagonalizable()
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n matrix with real entries",
    "¬Q: The minimal polynomial of A has repeated roots"
]

N_HYP = 1
NEG_Q_INDEX = 1