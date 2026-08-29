import sympy
from sympy.ntheory import isprime

def conditions(witness) -> list[bool]:
    try:
        p = int(witness)
    except Exception:
        return [False, False]
        
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False
        
    try:
        if h1:
            S = sum(pow(i, -1, p) for i in range(1, p))
            neg_q = (S % p) != 0
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "¬Q: S is not congruent to 0 mod p"
]

N_HYP = 1
NEG_Q_INDEX = 1