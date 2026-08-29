import sympy
from sympy import eye, zeros, Matrix

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: x^n = 0 for some positive integer n
    h1_ok = False
    try:
        zero_elem = witness * 0
        for n in range(1, 21):
            if witness**n == zero_elem:
                h1_ok = True
                break
    except Exception:
        h1_ok = False

    # ¬Q: x != 0
    neg_q_ok = False
    try:
        zero_elem = witness * 0
        neg_q_ok = bool(witness != zero_elem)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: x^n = 0 for some positive integer n",
    "¬Q: x != 0"
]

N_HYP = 1
NEG_Q_INDEX = 1