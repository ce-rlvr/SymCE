import sympy
from sympy.ntheory import isprime

def conditions(witness):
    try:
        a, p = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False
        
    try:
        h2 = isinstance(a, int) or isinstance(a, sympy.Integer)
    except Exception:
        h2 = False
        
    try:
        if h1 and h2:
            a_int = int(a)
            p_int = int(p)
            # p is prime, so p >= 2, meaning p - 2 >= 0.
            # Thus pow() will not raise a ValueError for negative exponent.
            val = (a_int * pow(a_int, p_int - 2, p_int)) % p_int
            neg_q = bool(val != 1)
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: a is an integer",
    "¬Q: a * a^{p-2} is not congruent to 1 mod p"
]

N_HYP = 2
NEG_Q_INDEX = 2