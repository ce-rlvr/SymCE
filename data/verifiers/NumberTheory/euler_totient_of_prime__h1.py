import sympy
from sympy.ntheory import totient

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (int, sympy.Integer)):
            return [False]
        p = int(witness)
        neg_q = bool(totient(p) != p - 1)
    except Exception:
        neg_q = False
    
    return [neg_q]

CONDITION_LABELS = ["¬Q: phi(p) != p - 1"]
N_HYP = 0
NEG_Q_INDEX = 0