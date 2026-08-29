import sympy

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False]
        a, b, c = witness
    except Exception:
        return [False, False]
    
    try:
        h1 = False
        if all(isinstance(x, (int, sympy.Integer)) for x in (a, b, c)):
            if a > 0 and b > 0 and c > 0:
                h1 = True
    except Exception:
        h1 = False
        
    try:
        neg_q = bool(a == b)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a, b, and c are strictly positive integers",
    "¬Q: a = b"
]

N_HYP = 1
NEG_Q_INDEX = 1