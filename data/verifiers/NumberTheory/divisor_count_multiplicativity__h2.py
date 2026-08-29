import sympy

def conditions(witness):
    try:
        m, n = witness
    except Exception:
        return [False, False]
    
    try:
        h1 = isinstance(m, (int, sympy.Integer)) and isinstance(n, (int, sympy.Integer)) and m > 0 and n > 0
    except Exception:
        h1 = False
        
    try:
        neg_q = sympy.divisor_count(m * n) != sympy.divisor_count(m) * sympy.divisor_count(n)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: m and n are positive integers",
    "¬Q: d(mn) != d(m)d(n)"
]

N_HYP = 1
NEG_Q_INDEX = 1