import math
import sympy

def conditions(witness):
    try:
        p = int(witness)
    except Exception:
        return [False, False]
    
    try:
        h1 = bool(sympy.isprime(p))
    except Exception:
        h1 = False
        
    try:
        exists = False
        if p >= 0:
            limit_y = math.isqrt(p // 3)
            for y in range(limit_y + 1):
                rem = p - 3 * y**2
                if rem >= 0:
                    x = math.isqrt(rem)
                    if x * x == rem:
                        exists = True
                        break
        
        mod_1 = (p % 3 == 1)
        neg_q = bool(exists != mod_1)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "¬Q: (exists x, y: p = x^2 + 3y^2) is not equivalent to (p ≡ 1 mod 3)"
]

N_HYP = 1
NEG_Q_INDEX = 1