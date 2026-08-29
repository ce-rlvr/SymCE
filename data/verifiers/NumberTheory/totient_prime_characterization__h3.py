import sympy
from sympy import isprime

# Top-level setup
# (no named bindings needed for number theory)

def conditions(witness) -> list[bool]:
    # H_1: n is an integer
    try:
        h1 = int(witness) == witness
    except Exception:
        h1 = False

    # H_2: n > 1
    try:
        h2 = bool(witness > 1)
    except Exception:
        h2 = False

    # neg_Q: n is NOT a prime number
    try:
        neg_q = not isprime(witness)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer",
    "H_2: n > 1",
    "¬Q: n is not a prime number"
]

N_HYP = 2
NEG_Q_INDEX = 2