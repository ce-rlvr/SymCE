import sympy
from sympy import gcd

def conditions(witness) -> list[bool]:
    try:
        a, b, c = witness
    except Exception:
        return [False]
    
    try:
        lhs = gcd(a, gcd(b, c))
        rhs = gcd(gcd(a, b), c)
        neg_q = bool(lhs != rhs)
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: gcd(a, gcd(b, c)) != gcd(gcd(a, b), c)"
]

N_HYP = 0
NEG_Q_INDEX = 0