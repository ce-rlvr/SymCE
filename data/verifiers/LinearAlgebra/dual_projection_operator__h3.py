import sympy
from sympy.matrices import MatrixBase, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        h1 = isinstance(witness, MatrixBase) and witness.is_square
    except Exception:
        h1 = False

    try:
        if h1:
            P_star = witness.transpose()
            neg_q = bool(P_star * P_star != P_star)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: P is a linear operator on V (witness is a square matrix)",
    "¬Q: P* is not a projection operator (P* ∘ P* != P*)"
]

N_HYP = 1
NEG_Q_INDEX = 1