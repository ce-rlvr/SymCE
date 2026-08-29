import sympy
from sympy.ntheory import isprime

Z4 = 4
Z6 = 6
Z8 = 8
Z9 = 9
Z10 = 10
Z12 = 12

def conditions(witness) -> list[bool]:
    try:
        w = int(witness)
        h1 = w > 1
    except Exception:
        h1 = False

    try:
        w = int(witness)
        neg_q = not isprime(w)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is an Artinian ring",
    "¬Q: R is not a field"
]

N_HYP = 1
NEG_Q_INDEX = 1