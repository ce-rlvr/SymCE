import sympy
from sympy.ntheory import factorint, isprime

# Top-level setup: Integers can represent the rings Z/nZ.
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6
Z8 = 8
Z9 = 9

def conditions(witness) -> list[bool]:
    """
    Checks if the witness (interpreted as the ring Z/nZ for an integer n)
    satisfies the remaining hypotheses and falsifies the conclusion.
    """
    # H_1: R is a commutative ring
    try:
        n = int(witness)
        # Z/nZ is a valid commutative ring for n > 1
        h1_ok = (n > 1)
    except Exception:
        h1_ok = False

    # H_2: R is a local ring
    try:
        n = int(witness)
        if n > 1:
            # A finite commutative ring Z/nZ is local iff it has exactly one maximal ideal.
            # The maximal ideals of Z/nZ correspond to the prime factors of n.
            # Thus, Z/nZ is local iff n has exactly one distinct prime factor (i.e., n = p^k).
            factors = factorint(n)
            h2_ok = (len(factors) == 1)
        else:
            h2_ok = False
    except Exception:
        h2_ok = False

    # ¬Q: R is not a field
    try:
        n = int(witness)
        if n > 1:
            # Z/nZ is a field iff n is prime.
            neg_q_ok = not isprime(n)
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R is a local ring",
    "¬Q: R is not a field"
]

N_HYP = 2
NEG_Q_INDEX = 2