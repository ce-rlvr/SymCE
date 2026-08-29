import sympy
from sympy import isprime
from sympy.polys.domains import ZZ, QQ, RR, CC

# Top-level setup
# Witnesses for finite rings Z/nZ can be provided directly as integers n.
# For example, 4 represents the ring Z/4Z.

def conditions(witness) -> list[bool]:
    # Attempt to extract an integer n representing the ring Z/nZ
    try:
        if isinstance(witness, tuple) and len(witness) > 0:
            witness = witness[0]
    except Exception:
        pass

    try:
        if isinstance(witness, str):
            s = witness.strip()
            if s.startswith("Z/") and s.endswith("Z"):
                witness = int(s[2:-1])
            elif s.startswith("Z") and len(s) > 1:
                witness = int(s[1:])
    except Exception:
        pass

    # Handle standard infinite domains
    if witness == ZZ:
        # The ring of integers is not Artinian, and not simple
        return [False, True]
    if witness in (QQ, RR, CC):
        # Fields are Artinian and simple
        return [True, False]

    # Evaluate for Z/nZ
    try:
        n = int(witness)
        # Z/nZ is a finite ring for n >= 2, hence it is right Artinian.
        h1_ok = (n >= 2)
    except Exception:
        h1_ok = False

    try:
        n = int(witness)
        # Z/nZ is simple if and only if n is prime.
        # Thus, it is NOT simple when n is composite.
        neg_q_ok = (n >= 2) and not isprime(n)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a right Artinian ring",
    "¬Q: R is not a simple ring"
]

N_HYP = 1
NEG_Q_INDEX = 1