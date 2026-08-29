import math
import sympy

def conditions(witness):
    try:
        a, m = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = (isinstance(m, int) or isinstance(m, sympy.Integer)) and int(m) > 1
    except Exception:
        h1 = False
        
    try:
        h2 = isinstance(a, int) or isinstance(a, sympy.Integer)
    except Exception:
        h2 = False
        
    try:
        a_int = int(a)
        m_int = int(m)
        neg_q = math.gcd(a_int, m_int) != 1
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: m is an integer strictly greater than 1",
    "H_2: a is an integer",
    "¬Q: There does not exist a unique integer x modulo m such that ax ≡ 1 (mod m)"
]

N_HYP = 2
NEG_Q_INDEX = 2