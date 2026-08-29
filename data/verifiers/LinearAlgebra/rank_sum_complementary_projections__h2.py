import sympy
from sympy import eye, zeros
from sympy.matrices import MatrixBase

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        h1 = isinstance(witness, MatrixBase) and witness.is_square and (witness**2 == witness)
    except Exception:
        h1 = False

    try:
        if not (isinstance(witness, MatrixBase) and witness.is_square):
            neg_q = False
        else:
            n = witness.shape[0]
            I = eye(n)
            rank_P = witness.rank()
            rank_I_minus_P = (I - witness).rank()
            neg_q = bool((rank_P + rank_I_minus_P) != n)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: P is an n x n projection matrix (P^2 = P) over a field F",
    "¬Q: The sum of the rank of P and the rank of I - P is not exactly equal to n"
]

N_HYP = 1
NEG_Q_INDEX = 1