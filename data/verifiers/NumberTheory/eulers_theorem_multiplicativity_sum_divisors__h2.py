import sympy
from sympy.ntheory import divisor_sigma

def conditions(witness):
    try:
        if len(witness) != 2:
            return [False, False]
        m, n = witness
    except Exception:
        return [False, False]
        
    try:
        h1 = isinstance(m, (int, sympy.Integer)) and isinstance(n, (int, sympy.Integer)) and m > 0 and n > 0
    except Exception:
        h1 = False
        
    try:
        neg_q = bool(divisor_sigma(m * n) != divisor_sigma(m) * divisor_sigma(n))
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: m and n are positive integers",
    "¬Q: sigma(mn) != sigma(m)sigma(n)"
]

N_HYP = 1
NEG_Q_INDEX = 1