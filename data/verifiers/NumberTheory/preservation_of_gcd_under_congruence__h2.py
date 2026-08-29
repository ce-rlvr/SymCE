import math
import sympy

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 3:
            return [False, False]
        a, b, m = witness
    except Exception:
        return [False, False]
    
    try:
        h1 = (isinstance(a, (int, sympy.Integer)) and 
              isinstance(b, (int, sympy.Integer)) and 
              isinstance(m, (int, sympy.Integer)) and 
              int(m) > 0)
    except Exception:
        h1 = False
        
    try:
        neg_q = math.gcd(int(a), int(m)) != math.gcd(int(b), int(m))
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a, b, m are integers with m > 0",
    "¬Q: gcd(a, m) != gcd(b, m)"
]

N_HYP = 1
NEG_Q_INDEX = 1