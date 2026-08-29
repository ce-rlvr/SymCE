import sympy
import math

def conditions(witness):
    try:
        n = int(witness)
    except Exception:
        return [False]
        
    try:
        lhs = sum(math.gcd(k, n) for k in range(1, n + 1))
        rhs = sum(d * sympy.totient(n // d) for d in sympy.divisors(n))
        neg_q = (lhs != rhs)
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: sum_{k=1}^n gcd(k, n) != sum_{d|n} d * phi(n/d)"
]

N_HYP = 0
NEG_Q_INDEX = 0