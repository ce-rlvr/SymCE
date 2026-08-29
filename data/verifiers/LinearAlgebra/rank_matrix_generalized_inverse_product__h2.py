import sympy
from sympy import Matrix, eye, zeros
from sympy.matrices import MatrixBase

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            A = witness['A']
            G = witness['G']
        elif isinstance(witness, (list, tuple)) and len(witness) >= 2:
            A = witness[0]
            G = witness[1]
        else:
            return [False, False]
    except Exception:
        return [False, False]

    try:
        h1_ok = isinstance(A, MatrixBase) and isinstance(G, MatrixBase) and A.cols == G.rows
    except Exception:
        h1_ok = False

    try:
        neg_q_ok = (A * G).rank() != A.rank()
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: A is an m x n matrix and G is a matrix such that AG is defined",
    "¬Q: The rank of AG is not equal to the rank of A"
]

N_HYP = 1
NEG_Q_INDEX = 1