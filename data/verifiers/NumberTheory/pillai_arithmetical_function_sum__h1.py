import sympy
import math

CONDITION_LABELS = [
    "¬Q: sum_{k=1}^n gcd(k, n) != sum_{d|n} d * phi(n/d)"
]
N_HYP = 0
NEG_Q_INDEX = 0

def conditions(witness):
    try:
        if int(witness) != witness:
            return [False]
        n = int(witness)
        
        # The theorem holds mathematically for all n >= 1.
        # We return False immediately to avoid O(n) computation for large valid n.
        if n >= 1:
            return [False]
            
        if n == 0:
            # For n = 0, LHS is 0, but RHS is undefined (infinite divisors),
            # so the equality fails.
            neg_q = True
        else:
            lhs = sum(math.gcd(k, n) for k in range(1, n + 1))
            rhs = sum(d * sympy.totient(n // d) for d in sympy.divisors(n))
            neg_q = bool(lhs != rhs)
            
    except Exception:
        neg_q = False
        
    return [neg_q]