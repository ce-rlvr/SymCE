import math
from sympy.ntheory import isprime, primitive_root

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
        if not h1:
            neg_q = False
        elif p > 100000:
            neg_q = False
        else:
            g = primitive_root(p)
            prod = 1
            for k in range(1, p):
                if math.gcd(k, p - 1) == 1:
                    root = pow(int(g), k, p)
                    prod = (prod * root) % p
            neg_q = bool(prod != 1)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "¬Q: The product of all primitive roots modulo p is not congruent to 1 (mod p)"
]

N_HYP = 1
NEG_Q_INDEX = 1