import sympy
from sympy import *

def conditions(witness):
    try:
        if isinstance(witness, dict):
            a = witness['a']
            b = witness['b']
            c = witness['c']
            m = witness['m']
            x = witness['x']
        elif hasattr(witness, '__getitem__') and len(witness) == 5:
            a, b, c, m, x = witness
        else:
            return [False, False, False]
            
        def is_int(v):
            try:
                return int(v) == v and not isinstance(v, bool)
            except Exception:
                return False

        h1 = is_int(a) and is_int(b) and is_int(c) and is_int(m) and is_int(x)
        
        if not h1:
            return [False, False, False]
            
        a = int(a)
        b = int(b)
        c = int(c)
        m = int(m)
        x = int(x)
        
        h2 = m > 0
        
        y = x - c
        neg_q = (a * y) % m != (b - a * c) % m
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: a, b, c, m, x are integers",
    "H_2: m > 0",
    "¬Q: y = x - c is not a solution to ay ≡ b - ac (mod m)"
]

N_HYP = 2
NEG_Q_INDEX = 2