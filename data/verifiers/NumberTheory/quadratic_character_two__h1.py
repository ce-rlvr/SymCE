import sympy
from sympy.ntheory import legendre_symbol

def conditions(witness):
    try:
        if isinstance(witness, str):
            p = int(witness)
        elif isinstance(witness, (int, sympy.Integer)):
            p = int(witness)
        else:
            return [False]
    except Exception:
        return [False]
        
    try:
        if p % 8 in (1, 7):
            q_holds = (legendre_symbol(2, p) == 1)
        elif p % 8 in (3, 5):
            q_holds = (legendre_symbol(2, p) == -1)
        else:
            q_holds = True
    except Exception:
        q_holds = False

    neg_q = not q_holds
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The Legendre symbol (2/p) is not 1 for p=1,7 mod 8, or not -1 for p=3,5 mod 8"
]

N_HYP = 0
NEG_Q_INDEX = 0