import sympy
from sympy import eye, Matrix

I2 = eye(2)
I3 = eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        P1, P2 = witness
        P1 = Matrix(P1)
        P2 = Matrix(P2)
    except Exception:
        return [False, False, False]

    try:
        h1 = P1.is_square and P2.is_square and P1.shape == P2.shape
    except Exception:
        h1 = False

    try:
        h2 = h1 and (P2 == P2.H) and (P2**2 == P2)
    except Exception:
        h2 = False

    try:
        if not h1:
            neg_q = False
        else:
            n = P1.shape[0]
            I = eye(n)
            invertible = (I - P1 * P2).det() != 0
            
            rank_P1 = P1.rank()
            rank_P2 = P2.rank()
            rank_join = P1.row_join(P2).rank()
            intersection_trivial = (rank_join == rank_P1 + rank_P2)
            
            neg_q = bool(invertible != intersection_trivial)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional inner product space",
    "H_2: P_2 is an orthogonal projection operator on V",
    "¬Q: The equivalence between invertibility of I - P_1 P_2 and trivial intersection of ranges fails"
]

N_HYP = 2
NEG_Q_INDEX = 2