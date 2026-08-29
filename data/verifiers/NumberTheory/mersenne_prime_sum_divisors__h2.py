import sympy
from sympy.ntheory import isprime, divisor_sigma

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
        val = divisor_sigma(2**p - 1)
        neg_q = bool(val != 2**p)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "¬Q: sigma(2^p - 1) != 2^p"
]

N_HYP = 1
NEG_Q_INDEX = 1