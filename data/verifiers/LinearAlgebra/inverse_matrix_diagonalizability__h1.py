import sympy
from sympy import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H_1: A is diagonalizable
    try:
        h1_ok = (witness.is_diagonalizable() == True)
    except Exception:
        h1_ok = False

    # H_2: A is invertible (det(A) != 0)
    try:
        h2_ok = (witness.det() != 0)
    except Exception:
        h2_ok = False

    # neg_Q: A^{-1} is NOT diagonalizable
    try:
        if h2_ok:
            inv_A = witness.inv()
            neg_q_ok = (inv_A.is_diagonalizable() == False)
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: A is diagonalizable",
    "H_2: A is invertible",
    "¬Q: A^{-1} is not diagonalizable"
]

N_HYP = 2
NEG_Q_INDEX = 2