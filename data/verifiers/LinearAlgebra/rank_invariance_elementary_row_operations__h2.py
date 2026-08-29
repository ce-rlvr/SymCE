import sympy
from sympy import eye, zeros
from sympy.matrices import MatrixBase

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            A = witness['A']
            B = witness['B']
        else:
            A, B = witness
    except Exception:
        return [False, False]

    try:
        h1_ok = isinstance(A, MatrixBase)
    except Exception:
        h1_ok = False

    try:
        neg_q_ok = A.rank() != B.rank()
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: A is an m x n matrix over a field F",
    "¬Q: The rank of A is not equal to the rank of B"
]

N_HYP = 1
NEG_Q_INDEX = 1