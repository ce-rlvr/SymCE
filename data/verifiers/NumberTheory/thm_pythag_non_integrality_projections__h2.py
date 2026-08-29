import math

def conditions(witness):
    try:
        a, b, c = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        a_int = int(a)
        b_int = int(b)
        c_int = int(c)
        h1 = (a_int == a) and (b_int == b) and (c_int == c)
        if isinstance(a, bool) or isinstance(b, bool) or isinstance(c, bool):
            h1 = False
    except Exception:
        h1 = False
        
    try:
        h2 = (a**2 + b**2 == c**2)
    except Exception:
        h2 = False
        
    try:
        h3 = (math.gcd(math.gcd(int(a), int(b)), int(c)) == 1)
    except Exception:
        h3 = False
        
    try:
        a_i, b_i, c_i = int(a), int(b), int(c)
        neg_q = (c_i != 0) and ((a_i**2 % c_i == 0) or (b_i**2 % c_i == 0))
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: a, b, c are integers",
    "H_2: a^2 + b^2 = c^2",
    "H_3: gcd(a, b, c) = 1",
    "¬Q: p = a^2/c or q = b^2/c is an integer"
]

N_HYP = 3
NEG_Q_INDEX = 3