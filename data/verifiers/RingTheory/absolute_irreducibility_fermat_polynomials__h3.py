import sympy
from sympy import symbols, GF, QQ, ZZ

X, Y, Z = symbols('X Y Z')

def conditions(witness):
    try:
        n, K = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = isinstance(n, (int, sympy.Integer)) and n >= 3
    except Exception:
        h1 = False
        
    try:
        h2 = hasattr(K, 'is_Field') and K.is_Field
    except Exception:
        h2 = False
        
    try:
        char = 0
        if hasattr(K, 'characteristic'):
            c = K.characteristic
            char = c() if callable(c) else c
        elif hasattr(K, 'char'):
            c = K.char
            char = c() if callable(c) else c
            
        neg_q = bool(char > 0 and n % char == 0)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer with n >= 3",
    "H_2: K is a field",
    "not Q: X^n + Y^n + Z^n is not absolutely irreducible over K"
]

N_HYP = 2
NEG_Q_INDEX = 2