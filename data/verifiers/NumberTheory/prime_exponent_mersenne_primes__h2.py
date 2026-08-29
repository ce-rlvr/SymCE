import sympy
from sympy.ntheory import isprime

# No specific named bindings needed for this number theory conjecture.

def conditions(witness) -> list[bool]:
    try:
        h1 = (isinstance(witness, int) or isinstance(witness, sympy.Integer)) and witness > 1
    except Exception:
        h1 = False

    try:
        neg_q = not isprime(witness)
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: n is an integer strictly greater than 1",
    "¬Q: n is not a prime number"
]

N_HYP = 1
NEG_Q_INDEX = 1