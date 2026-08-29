import sympy
from sympy import Matrix, MatrixBase, zeros, eye

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, (list, tuple)):
            Q = Matrix(witness)
        else:
            Q = witness
    except Exception:
        Q = witness

    try:
        h1 = isinstance(Q, MatrixBase) and Q.is_square and all(e.is_real is True for e in Q)
    except Exception:
        h1 = False

    try:
        h2 = isinstance(Q, MatrixBase) and Q.shape[0] >= 1
    except Exception:
        h2 = False

    try:
        if isinstance(Q, MatrixBase) and Q.is_square:
            n = Q.shape[0]
            neg_q = bool((Q**n) == zeros(n, n))
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: Q is an n x n real matrix",
    "H_2: n >= 1",
    "¬Q: Q is a nilpotent matrix"
]

N_HYP = 2
NEG_Q_INDEX = 2