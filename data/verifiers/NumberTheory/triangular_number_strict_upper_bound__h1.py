import sympy
from sympy.ntheory import divisor_sigma

def conditions(witness):
    try:
        n = int(witness)
        if n < 1:
            neg_q = False
        else:
            sigma_n = divisor_sigma(n)
            neg_q = bool(sigma_n >= n * (n + 1) // 2)
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: sigma(n) >= n(n+1)/2"
]

N_HYP = 0
NEG_Q_INDEX = 0