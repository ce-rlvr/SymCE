import sympy as sp
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if not (isinstance(witness, (tuple, list)) and len(witness) == 2):
            return [False, False, False]
        P1, P2 = witness
        if not (isinstance(P1, Matrix) and isinstance(P2, Matrix)):
            return [False, False, False]
        if not (P1.is_square and P2.is_square and P1.shape == P2.shape):
            return [False, False, False]
        h1 = True
    except Exception:
        h1 = False

    try:
        diff = P1 * P1 - P1
        h2 = all((x == 0 or sp.simplify(x) == 0) for x in diff)
    except Exception:
        h2 = False

    try:
        diff_lhs = P1 * P2 - P2
        lhs = all((x == 0 or sp.simplify(x) == 0) for x in diff_lhs)
        
        null_P1 = P1.nullspace()
        rhs = True
        for v in null_P1:
            prod = P2 * v
            if not all((x == 0 or sp.simplify(x) == 0) for x in prod):
                rhs = False
                break
                
        neg_q = (lhs != rhs)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is a vector space and P1, P2 are operators on V",
    "H_2: P_1 is a projection operator on V",
    "¬Q: (P_1 P_2 = P_2) is not equivalent to (Null(P_1) is a subset of Null(P_2))"
]

N_HYP = 2
NEG_Q_INDEX = 2