import sympy
from sympy.ntheory import legendre_symbol

CONDITION_LABELS = [
    "¬Q: The Legendre symbol (-2/p) does not equal 1 when p = 1,3 mod 8, or does not equal -1 when p = 5,7 mod 8"
]

N_HYP = 0
NEG_Q_INDEX = 0

def conditions(witness):
    try:
        p = int(witness)
        if p != witness:
            return [False]
    except Exception:
        return [False]
    
    try:
        if p % 8 in (1, 3):
            q_holds = (legendre_symbol(-2, p) == 1)
        elif p % 8 in (5, 7):
            q_holds = (legendre_symbol(-2, p) == -1)
        else:
            q_holds = True
    except Exception:
        q_holds = False
        
    neg_q = not q_holds
    return [neg_q]