import sympy
from sympy.ntheory import factorint
from sympy.abc import x, y, z

# Top-level setup
# The witness is expected to be an integer n >= 2, representing the ring Z/nZ.
# Z/nZ is always a commutative Artinian ring.

def conditions(witness) -> list[bool]:
    try:
        n = int(witness)
        # Z/nZ is a commutative Artinian ring for any integer n >= 2.
        h1 = (n >= 2)
    except Exception:
        h1 = False

    try:
        if h1:
            factors = factorint(n)
            # The conclusion "The maximal ideal m is nilpotent" implies there is a 
            # unique maximal ideal and it is nilpotent.
            # In Z/nZ, the maximal ideals correspond to prime factors of n.
            # There is a unique maximal ideal iff n has exactly one prime factor.
            # If n has >1 prime factors, the ring is not local, and no maximal ideal is nilpotent.
            # Thus, the conclusion fails (neg_q is True) iff n has >1 prime factors.
            neg_q = len(factors) > 1
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative Artinian ring",
    "¬Q: The maximal ideal is not nilpotent (or not unique)"
]

N_HYP = 1
NEG_Q_INDEX = 1