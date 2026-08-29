import sympy
import sympy.ntheory
import math

def conditions(witness):
    try:
        if len(witness) != 2:
            return [False, False, False]
        m, n = witness
        m_int = int(m)
        n_int = int(n)
        if m_int != m or n_int != n:
            return [False, False, False]
        m, n = m_int, n_int
    except Exception:
        return [False, False, False]
    
    try:
        h1 = (math.gcd(m, n) == 1)
    except Exception:
        h1 = False
        
    h2 = True
    
    try:
        if m <= 0 or n <= 0:
            neg_q = True
        else:
            lhs = sympy.ntheory.mobius(m * n)
            rhs = sympy.ntheory.mobius(m) * sympy.ntheory.mobius(n)
            neg_q = bool(lhs != rhs)
    except Exception:
        neg_q = True
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: \\gcd(m, n) = 1",
    "H_2: \\mu is the Mobius function",
    "¬Q: \\mu(mn) \\neq \\mu(m)\\mu(n) (or undefined)"
]

N_HYP = 2
NEG_Q_INDEX = 2