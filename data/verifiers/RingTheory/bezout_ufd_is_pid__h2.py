import sympy
from sympy import ZZ, QQ, RR, CC
from sympy.abc import x, y, z

# Standard ring domains for witness expressions
ZZ_x = ZZ.poly_ring(x)
QQ_x = QQ.poly_ring(x)
ZZ_x_y = ZZ.poly_ring(x, y)
QQ_x_y = QQ.poly_ring(x, y)

def conditions(witness):
    try:
        # Check if the witness is explicitly a Unique Factorization Domain
        h1 = (witness.is_UFD is True)
    except Exception:
        h1 = False

    try:
        # Check if the witness is explicitly NOT a Principal Ideal Domain
        neg_q = (witness.is_PID is False)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "¬Q: R is not a Principal Ideal Domain"
]

N_HYP = 1
NEG_Q_INDEX = 1