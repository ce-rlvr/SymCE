import sympy
from sympy import ZZ, QQ
from sympy.abc import x
from sympy.matrices import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        char_R = witness.characteristic
        if callable(char_R):
            char_R = char_R()
        try:
            Rx = witness.poly_ring(x)
        except Exception:
            Rx = witness[x]
        char_Rx = Rx.characteristic
        if callable(char_Rx):
            char_Rx = char_Rx()
        neg_q = bool(char_R != char_Rx)
    except Exception:
        neg_q = False
    return [neg_q]

CONDITION_LABELS = ["not Q: The characteristic of R poly ring is not equal to the characteristic of R"]
N_HYP = 0
NEG_Q_INDEX = 0