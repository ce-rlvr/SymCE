import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        A, B, C = witness
        h1 = False
        if hasattr(A, 'is_square') and A.is_square and hasattr(C, 'is_square') and C.is_square:
            if hasattr(B, 'rows') and hasattr(B, 'cols'):
                if B.rows == A.rows and B.cols == C.cols:
                    h1 = True
    except Exception:
        h1 = False

    try:
        A, B, C = witness
        h2 = bool(A.is_zero_matrix)
    except Exception:
        h2 = False

    try:
        A, B, C = witness
        neg_q = not bool(B.is_zero_matrix)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: M is partitioned into block form",
    "H_2: The principal block A is a zero matrix",
    "¬Q: The off-diagonal block B is not a zero matrix"
]

N_HYP = 2
NEG_Q_INDEX = 2