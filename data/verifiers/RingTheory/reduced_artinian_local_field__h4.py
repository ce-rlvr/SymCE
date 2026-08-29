import sympy
from sympy.ntheory import factorint, isprime
from sympy.abc import x, y, z

# Top-level setup
# The witness is expected to be an integer n > 1, representing the ring Z/nZ.
# String representations like "Z/4Z" are also supported.

def conditions(witness) -> list[bool]:
    # Parse string representations of Z/nZ if provided
    if isinstance(witness, str):
        w_str = witness.strip().replace(" ", "")
        if w_str.startswith("Z/") and w_str.endswith("Z"):
            try:
                witness = int(w_str[2:-1])
            except ValueError:
                pass

    try:
        n = int(witness)
    except Exception:
        return [False, False, False, False]

    try:
        # H_1: R is a commutative ring
        # Z/nZ is a commutative ring for n > 1
        h1 = (n > 1)
    except Exception:
        h1 = False

    try:
        # H_2: R is a local ring
        # Z/nZ is local iff it has a unique maximal ideal.
        # The maximal ideals of Z/nZ correspond to the prime factors of n.
        # Thus, Z/nZ is local iff n has exactly one prime factor (i.e., n = p^k).
        if n > 1:
            facs = factorint(n)
            h2 = (len(facs) == 1)
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        # H_3: R is an Artinian ring
        # Z/nZ is a finite ring, and all finite rings are Artinian.
        h3 = (n > 1)
    except Exception:
        h3 = False

    try:
        # ¬Q: R is not a field
        # Z/nZ is a field iff n is prime.
        if n > 1:
            neg_q = not isprime(n)
        else:
            neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R is a local ring",
    "H_3: R is an Artinian ring",
    "¬Q: R is not a field"
]

N_HYP = 3
NEG_Q_INDEX = 3