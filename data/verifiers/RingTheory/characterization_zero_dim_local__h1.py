import sympy
from sympy.ntheory import primefactors

# Setup: Integer n represents the ring Z/nZ.
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z8 = 8
Z9 = 9
Z10 = 10
Z12 = 12

def conditions(witness) -> list[bool]:
    # H_1: The Krull dimension of R is 0
    # For R = Z/nZ (n >= 2), R is a finite commutative ring, so its Krull dimension is always 0.
    try:
        n = int(witness)
        h1_ok = (n >= 2)
    except Exception:
        h1_ok = False

    # ¬Q: \mathfrak{m} is NOT the unique prime ideal of R
    # In Z/nZ, the prime ideals correspond to the prime factors of n.
    # The conclusion fails if there is not exactly 1 prime ideal (i.e., n is not a prime power).
    try:
        n = int(witness)
        if n >= 2:
            factors = primefactors(n)
            neg_q_ok = (len(factors) != 1)
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: The Krull dimension of R is 0",
    "¬Q: R does not have a unique prime ideal"
]

N_HYP = 1
NEG_Q_INDEX = 1