import sympy
from sympy.ntheory import factorint

# Top-level setup
# (No named bindings needed for this domain)

def conditions(witness) -> list[bool]:
    n = None
    k = None
    try:
        if isinstance(witness, (tuple, list)):
            n = int(witness[0])
            if len(witness) > 1:
                k = int(witness[1])
        else:
            n = int(witness)
    except Exception:
        pass

    try:
        h1 = False
        if n is not None:
            h1 = bool(n > 1)
    except Exception:
        h1 = False

    try:
        neg_q = False
        if n is not None and h1:
            factors = factorint(n)
            # If k is not explicitly provided in the witness, it refers to the 
            # total number of prime factors of n (counted with multiplicity),
            # which is the standard meaning in the original true theorem 
            # (where n was restricted to be square-free).
            if k is None:
                k = sum(factors.values())
            
            # The number of idempotents in Z/nZ is always 2^(number of distinct prime factors)
            idempotents = 2 ** len(factors)
            neg_q = bool(idempotents != 2**k)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer strictly greater than 1",
    "¬Q: The number of idempotent elements in Z/nZ is not 2^k"
]

N_HYP = 1
NEG_Q_INDEX = 1