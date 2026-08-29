import math
import sympy

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False]
        x, y, z = witness
        x = int(x)
        y = int(y)
        z = int(z)
    except Exception:
        return [False, False]
        
    try:
        h1 = (x**2 + y**2 + z**2 == 3 * x * y * z)
    except Exception:
        h1 = False
        
    try:
        neg_q = (math.gcd(x, y) != 1) or (math.gcd(y, z) != 1) or (math.gcd(x, z) != 1)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x^2 + y^2 + z^2 = 3xyz",
    "¬Q: gcd(x, y) != 1 or gcd(y, z) != 1 or gcd(x, z) != 1"
]

N_HYP = 1
NEG_Q_INDEX = 1