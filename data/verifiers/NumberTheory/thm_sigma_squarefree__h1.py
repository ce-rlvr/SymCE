import sympy
import math

def conditions(witness) -> list[bool]:
    try:
        n = int(witness)
        if n != witness:
            return [False, False]
    except Exception:
        return [False, False]
    
    try:
        h1 = sympy.is_square_free(n)
    except Exception:
        h1 = False
        
    try:
        if n <= 0:
            # Mathematically, the sum-of-divisors function sigma(n) is defined 
            # only for positive integers. For n <= 0, the equation fails.
            neg_q = True
        else:
            lhs = sympy.divisor_sigma(n)
            rhs = math.prod(p + 1 for p in sympy.primefactors(n))
            neg_q = bool(lhs != rhs)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a square-free integer",
    "¬Q: sigma(n) != prod_{p|n} (p+1)"
]

N_HYP = 1
NEG_Q_INDEX = 1