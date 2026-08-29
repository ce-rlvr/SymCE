import sympy
import math

# Top-level setup
ZZ = sympy.ZZ
QQ = sympy.QQ
RR = sympy.RR
CC = sympy.CC

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "Let R be a left Noetherian ring. The matrix ring M_n(R) is a left Noetherian ring."
    (The dropped hypothesis is that n is a finite positive integer).
    """
    # Unpack witness
    if isinstance(witness, tuple) and len(witness) == 2:
        R, n = witness
    else:
        # If only n is provided, assume a standard Noetherian ring like ZZ
        R = ZZ
        n = witness

    # H_1: R is a left Noetherian ring
    try:
        if R in (ZZ, QQ, RR, CC):
            h1_ok = True
        elif getattr(R, 'is_Noetherian', False) or getattr(R, 'is_left_Noetherian', False):
            h1_ok = True
        elif hasattr(R, 'is_ring') and R.is_ring:
            h1_ok = True
        else:
            h1_ok = False
    except Exception:
        h1_ok = False

    # ¬Q: The matrix ring M_n(R) is NOT a left Noetherian ring
    # This happens when n is infinite.
    try:
        neg_q_ok = (n == sympy.oo) or (n == math.inf) or (str(n).lower() in ['oo', 'infinity', 'inf'])
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a left Noetherian ring",
    "¬Q: The matrix ring M_n(R) is not a left Noetherian ring"
]

N_HYP = 1
NEG_Q_INDEX = 1