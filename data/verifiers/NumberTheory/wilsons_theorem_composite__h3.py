import math
import sympy

def conditions(witness) -> list[bool]:
    try:
        h1 = int(witness) == witness
    except Exception:
        h1 = False

    try:
        h2 = witness > 4
    except Exception:
        h2 = False

    try:
        n = int(witness)
        neg_q = (math.factorial(n - 1) % n) != 0
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: n is an integer",
    "H_2: n > 4",
    "¬Q: n does not divide (n-1)!"
]

N_HYP = 2
NEG_Q_INDEX = 2