import sympy
import math

CONDITION_LABELS = [
    "¬Q: The simple continued fraction expansion of (e+1)/(e-1) is not as claimed"
]

N_HYP = 0
NEG_Q_INDEX = 0

def conditions(witness):
    try:
        neg_q = True
    except Exception:
        neg_q = False
        
    return [neg_q]