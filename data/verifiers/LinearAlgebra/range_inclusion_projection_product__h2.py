import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        P1, P2 = witness
        P1 = Matrix(P1)
        P2 = Matrix(P2)
    except Exception:
        return [False, False, False]
        
    # H1: V is a vector space (P1, P2 are square matrices of the same size)
    try:
        h1 = bool(P1.is_square and P2.is_square and P1.shape == P2.shape)
    except Exception:
        h1 = False
        
    # H2: P2 is a projection operator on V
    try:
        h2 = h1 and bool(P2 * P2 == P2)
    except Exception:
        h2 = False
        
    # neg_Q: P1 P2 = P1 iff Range(P1) is a subset of Range(P2)
    try:
        if not h1:
            neg_q = False
        else:
            eq_cond = bool(P1 * P2 == P1)
            # Range(P1) is a subset of Range(P2) iff rank([P2, P1]) == rank(P2)
            range_cond = bool(P2.row_join(P1).rank() == P2.rank())
            neg_q = (eq_cond != range_cond)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is a vector space (P1, P2 are square matrices of same size)",
    "H_2: P_2 is a projection operator on V",
    "¬Q: (P_1 P_2 = P_1) is NOT equivalent to (Range(P_1) subseteq Range(P_2))"
]

N_HYP = 2
NEG_Q_INDEX = 2