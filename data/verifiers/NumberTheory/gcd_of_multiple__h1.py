import math
import sympy

# Top-level setup: no specific named objects needed for this number theory conjecture.

def conditions(witness) -> list[bool]:
    try:
        a, b = witness
        if int(a) != a or int(b) != b:
            return [False, False]
        a = int(a)
        b = int(b)
    except Exception:
        return [False, False]
    
    try:
        if a == 0:
            h1 = (b == 0)
        else:
            h1 = (b % a == 0)
    except Exception:
        h1 = False
        
    try:
        neg_q = (math.gcd(a, b) != a)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: a divides b",
    "¬Q: gcd(a, b) != a"
]

N_HYP = 1
NEG_Q_INDEX = 1