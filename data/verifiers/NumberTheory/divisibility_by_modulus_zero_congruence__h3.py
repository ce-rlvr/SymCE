import sympy

def conditions(witness) -> list[bool]:
    try:
        m, a = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = isinstance(m, (int, sympy.Integer)) and m > 0
    except Exception:
        h1 = False
        
    try:
        h2 = isinstance(a, (int, sympy.Integer))
    except Exception:
        h2 = False
        
    try:
        neg_q = (a % m) != 0
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: m is a positive integer",
    "H_2: a is an integer",
    "¬Q: m does not divide a"
]

N_HYP = 2
NEG_Q_INDEX = 2