import sympy as sp
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if len(witness) != 2:
            return [False] * 5
        P1, P2 = witness
        P1 = Matrix(P1)
        P2 = Matrix(P2)
        if P1.shape != P2.shape or P1.rows != P1.cols:
            return [False] * 5
    except Exception:
        return [False] * 5

    h1 = True
    h2 = True

    try:
        h3 = bool(P2**2 == P2)
    except Exception:
        h3 = False

    try:
        h4 = bool(P1 * P2 == P2 * P1)
    except Exception:
        h4 = False

    try:
        C = P1 * P2
        cond1 = bool(C**2 == C)
        dim_int = P1.rank() + P2.rank() - P1.row_join(P2).rank()
        cond2 = bool(C.rank() == dim_int)
        neg_q = not (cond1 and cond2)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: V is a vector space",
    "H_2: P_1 and P_2 are linear operators on V",
    "H_3: P_2^2 = P_2",
    "H_4: P_1 P_2 = P_2 P_1",
    "¬Q: (P_1 P_2)^2 != P_1 P_2 or im(P_1 P_2) != im(P_1) \\cap im(P_2)"
]

N_HYP = 4
NEG_Q_INDEX = 4