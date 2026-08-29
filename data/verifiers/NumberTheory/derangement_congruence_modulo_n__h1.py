import sympy
import math

def conditions(witness):
    try:
        n = int(witness)
        if n != witness:
            return [False]
        
        if n < 0:
            return [False]
            
        dn = int(sympy.subfactorial(n))
        
        if n == 0:
            holds = (dn == 1)
        else:
            holds = (dn % n) == (((-1)**n) % n)
            
        neg_q = not holds
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: D_n is not congruent to (-1)^n mod n"
]

N_HYP = 0
NEG_Q_INDEX = 0