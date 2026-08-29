import sympy
from sympy.ntheory import isprime, legendre_symbol

def conditions(witness):
    try:
        a, p = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = bool(isinstance(p, (int, sympy.Integer)) and isprime(p) and p % 2 == 1)
    except Exception:
        h1 = False
        
    try:
        h2 = bool(isinstance(a, (int, sympy.Integer)))
    except Exception:
        h2 = False
        
    try:
        n = 0
        for k in range(1, (p - 1) // 2 + 1):
            res = (k * a) % p
            # Least positive residue is in the range [1, p]
            if res == 0:
                res = p
            if res > p / 2:
                n += 1
        leg = legendre_symbol(a, p)
        neg_q = bool(leg != (-1)**n)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is an odd prime",
    "H_2: a is an integer",
    "¬Q: The Legendre symbol (a/p) does not equal (-1)^n"
]

N_HYP = 2
NEG_Q_INDEX = 2