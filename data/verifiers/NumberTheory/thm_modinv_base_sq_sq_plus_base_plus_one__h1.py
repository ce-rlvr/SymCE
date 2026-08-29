import sympy
import math

def conditions(witness):
    try:
        a = int(witness)
        mod = a**2 + a + 1
        inv = pow(a**2, -1, mod)
        neg_q = bool(inv != a)
    except Exception:
        neg_q = False
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The modular inverse of a^2 modulo a^2 + a + 1 is not a"
]

N_HYP = 0
NEG_Q_INDEX = 0