import sympy
from sympy import isprime
from sympy.polys.domains import ZZ, QQ, RR, CC

# Top-level setup: named object bindings that the witness expression may reference.
# We define integers to represent the rings Z/nZ, which are the standard counterexamples.
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z8 = 8
Z9 = 9
Z10 = 10
Z12 = 12

def get_char(witness):
    """Helper to extract the characteristic from a ring or integer witness."""
    if hasattr(witness, 'characteristic'):
        val = witness.characteristic
        if callable(val):
            return int(val())
        return int(val)
    if hasattr(witness, 'char'):
        val = witness.char
        if callable(val):
            return int(val())
        return int(val)
    # If the witness is an integer n, we interpret it as the ring Z/nZ, 
    # which has characteristic n.
    return int(witness)

def conditions(witness) -> list[bool]:
    # H_1: The characteristic of R is not equal to 0.
    try:
        char = get_char(witness)
        h1 = (char != 0)
    except Exception:
        h1 = False

    # ¬Q: The characteristic of R is NOT a prime number.
    try:
        char = get_char(witness)
        neg_q = not isprime(char)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: The characteristic of R is not equal to 0",
    "¬Q: The characteristic of R is not a prime number"
]

N_HYP = 1
NEG_Q_INDEX = 1