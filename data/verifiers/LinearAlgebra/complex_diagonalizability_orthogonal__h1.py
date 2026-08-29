import sympy
from sympy import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if not hasattr(witness, 'is_square') or not witness.is_square:
            neg_q = False
        else:
            neg_q = not witness.is_diagonalizable()
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: Q is not diagonalizable over the field of complex numbers"
]

N_HYP = 0
NEG_Q_INDEX = 0