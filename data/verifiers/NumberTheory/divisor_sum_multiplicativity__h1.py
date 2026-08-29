import math
import sympy

def conditions(witness):
    try:
        m, n = witness
    except Exception:
        return [False, False]
    
    try:
        h1 = (math.gcd(int(m), int(n)) == 1)
    except Exception:
        h1 = False
        
    try:
        m_int = int(m)
        n_int = int(n)
        if m_int == 0 or n_int == 0:
            # sigma(0) is undefined, so the equality sigma(mn) = sigma(m)sigma(n) fails.
            neg_q = True
        else:
            lhs = sympy.divisor_sigma(abs(m_int * n_int))
            rhs = sympy.divisor_sigma(abs(m_int)) * sympy.divisor_sigma(abs(n_int))
            neg_q = bool(lhs != rhs)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: \\gcd(m, n) = 1",
    "¬Q: \\sigma(mn) \\neq \\sigma(m)\\sigma(n)"
]

N_HYP = 1
NEG_Q_INDEX = 1