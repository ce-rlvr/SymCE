import sympy
from sympy import Matrix, eye, zeros, I
from sympy.matrices import MatrixBase

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        h1 = isinstance(witness, MatrixBase)
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            A = witness
            rank_A = A.rank()
            rank_AtA = (A.T * A).rank()
            neg_q = bool(rank_AtA != rank_A)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is an m x n matrix",
    "¬Q: The rank of A^T A is not equal to the rank of A"
]

N_HYP = 1
NEG_Q_INDEX = 1