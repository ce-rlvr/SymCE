import sympy
import math
from sympy.ntheory import totient

CONDITION_LABELS = [
    "H_1: n >= 3",
    "¬Q: phi(n) is not an even integer"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        h1 = bool(witness >= 3)
    except Exception:
        h1 = False

    try:
        if int(witness) == witness:
            val = totient(int(witness))
            is_even_int = (val % 2 == 0)
        else:
            is_even_int = False
        neg_q = not is_even_int
    except Exception:
        neg_q = True

    return [h1, neg_q]