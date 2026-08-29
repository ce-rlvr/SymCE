import math
import sympy
from sympy.ntheory import totient

def conditions(witness) -> list[bool]:
    try:
        h1 = isinstance(witness, (int, sympy.Integer)) and int(witness) > 0
    except Exception:
        h1 = False

    try:
        n = int(witness)
        phi = int(totient(n))
        neg_q = phi > n - math.sqrt(n)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: phi(n) > n - sqrt(n)"
]

N_HYP = 1
NEG_Q_INDEX = 1