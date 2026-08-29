import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        h1 = isinstance(witness, sympy.MatrixBase)
    except Exception:
        h1 = False

    try:
        if h1:
            rank = witness.rank()
            injective = (rank == witness.cols)
            surjective = (rank == witness.rows)
            neg_q = (injective != surjective)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: T is a linear transformation between finite-dimensional vector spaces (represented by a matrix)",
    "¬Q: T is injective is not equivalent to T is surjective"
]

N_HYP = 1
NEG_Q_INDEX = 1