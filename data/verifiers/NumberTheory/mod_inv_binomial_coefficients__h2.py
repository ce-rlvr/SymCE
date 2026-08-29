import math
from sympy import isprime

def conditions(witness):
    try:
        p, k = witness
    except Exception:
        return [False, False, False]
    
    # H_1: p is a prime number
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False
        
    # H_2: 0 <= k <= p - 1
    try:
        h2 = bool(0 <= k <= p - 1)
    except Exception:
        h2 = False
        
    # neg_Q: The modular inverse of (p-1 choose k) modulo p is not congruent to (-1)^k (mod p)
    try:
        if int(p) != p or int(k) != k:
            # If p or k are not integers, the standard binomial coefficient or modular arithmetic fails.
            neg_q = True
        else:
            c = math.comb(int(p - 1), int(k))
            inv = pow(c, -1, int(p))
            expected = ((-1) ** int(k)) % int(p)
            neg_q = bool(inv != expected)
    except Exception:
        # If math.comb fails (e.g. negative arguments) or pow fails (no modular inverse exists),
        # the conclusion fails to hold, so its negation is True.
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: 0 <= k <= p - 1",
    "¬Q: The modular inverse of (p-1 choose k) modulo p is not congruent to (-1)^k (mod p)"
]

N_HYP = 2
NEG_Q_INDEX = 2