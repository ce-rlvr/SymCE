import sympy
import math
import itertools
import functools

def conditions(witness):
    try:
        a = int(witness)
        mod = a**2 + a + 1
        val = a + 1
        inv = pow(val, -1, mod)
        neg_q = bool(inv != (a**2 + 1))
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The modular inverse of a+1 modulo a^2+a+1 is not a^2+1"
]

N_HYP = 0
NEG_Q_INDEX = 0