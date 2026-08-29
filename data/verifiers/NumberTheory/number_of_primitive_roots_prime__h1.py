import sympy
import sympy.ntheory
import math

def conditions(witness):
    try:
        p = int(witness)
        if p <= 1:
            return [False]
        
        count = 0
        for a in range(1, p):
            if math.gcd(a, p) == 1:
                if sympy.ntheory.n_order(a, p) == p - 1:
                    count += 1
                    
        expected = sympy.totient(p - 1)
        neg_q = bool(count != expected)
        return [neg_q]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: The number of incongruent integers modulo p having multiplicative order p-1 is not exactly \phi(p-1)"
]

N_HYP = 0
NEG_Q_INDEX = 0