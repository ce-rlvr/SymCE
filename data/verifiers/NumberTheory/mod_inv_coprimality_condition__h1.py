import math
import sympy

def conditions(witness) -> list[bool]:
    try:
        a, b, m = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = isinstance(a, int) and isinstance(b, int)
    except Exception:
        h1 = False
        
    try:
        h2 = (a * b) % m == 1 % m
    except Exception:
        h2 = False
        
    try:
        neg_q = math.gcd(b, m) != 1
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a and b are integers",
    "H_2: a * b ≡ 1 (mod m)",
    "¬Q: gcd(b, m) != 1"
]

N_HYP = 2
NEG_Q_INDEX = 2