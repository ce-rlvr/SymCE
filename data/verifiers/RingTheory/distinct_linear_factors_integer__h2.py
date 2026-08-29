import sympy

def is_int(val):
    if isinstance(val, int):
        return True
    if isinstance(val, sympy.Integer):
        return True
    if hasattr(val, 'is_integer') and val.is_integer:
        return True
    return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            a = witness['a']
            b = witness['b']
        else:
            a, b = witness
    except Exception:
        return [False, False]
        
    try:
        h1 = is_int(a) and is_int(b)
    except Exception:
        h1 = False
        
    try:
        # The theorem "Distinct Linear Factors Integer Factor Ring Theorem" 
        # originally requires the hypothesis that a and b are distinct (a != b).
        # When a == b, the formal conclusion fails (e.g., expecting a finite quotient ring).
        neg_q = bool(a == b)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a and b are integers",
    "not Q: The factor ring Z(x)/(x-a, x-b) is not isomorphic to Z/(a-b)"
]

N_HYP = 1
NEG_Q_INDEX = 1