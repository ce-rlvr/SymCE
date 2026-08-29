import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        B = Matrix(witness)
        h1_ok = True
    except Exception:
        h1_ok = False

    try:
        B = Matrix(witness)
        left_rad_dim = B.shape[0] - B.rank()
        right_rad_dim = B.shape[1] - B.rank()
        neg_q_ok = bool(left_rad_dim != right_rad_dim)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space",
    "¬Q: The dimension of the left radical of B is not equal to the dimension of the right radical of B"
]

N_HYP = 1
NEG_Q_INDEX = 1