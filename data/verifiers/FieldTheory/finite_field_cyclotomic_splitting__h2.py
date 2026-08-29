import math
import sympy
from sympy.ntheory import factorint

# Top-level setup
# No specific named objects are required for this field theory witness,
# as the witness is expected to be a tuple of integers (q, n).

def conditions(witness):
    try:
        q, n = witness
        q = int(q)
        n = int(n)
    except Exception:
        return [False, False]
    
    # H_1: F_q is a finite field of order q (so q is a prime power)
    try:
        if q >= 2:
            factors = factorint(q)
            h1_ok = (len(factors) == 1)
        else:
            h1_ok = False
    except Exception:
        h1_ok = False
        
    # ¬Q: The conclusion fails.
    # The conclusion states the splitting field is F_{q^d} where d is the multiplicative order of q mod n.
    # This requires gcd(q, n) == 1 for d to be defined. If gcd(q, n) > 1, d is undefined and the conclusion fails.
    try:
        if h1_ok and n >= 1:
            neg_q_ok = (math.gcd(q, n) > 1)
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F_q is a finite field of order q",
    "¬Q: The conclusion fails (multiplicative order of q mod n is undefined because gcd(q, n) > 1)"
]

N_HYP = 1
NEG_Q_INDEX = 1