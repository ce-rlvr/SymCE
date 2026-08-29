import sympy
import math

def conditions(witness):
    try:
        if not isinstance(witness, (int, sympy.Integer)):
            return [False]
        n = int(witness)
        
        lhs = 0
        for k in range(1, n + 1):
            if math.gcd(k, n) == 1:
                lhs += math.gcd(k - 1, n)
                
        rhs = sympy.totient(n) * sympy.divisor_count(n)
        neg_q = bool(lhs != rhs)
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: sum_{1<=k<=n, gcd(k,n)=1} gcd(k-1, n) != phi(n) tau(n)"
]
N_HYP = 0
NEG_Q_INDEX = 0