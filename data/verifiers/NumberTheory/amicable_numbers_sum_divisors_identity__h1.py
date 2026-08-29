import sympy
from sympy.ntheory import divisor_sigma

def conditions(witness):
    try:
        m, n = witness
        m = int(m)
        n = int(n)
        if m <= 0 or n <= 0:
            return [False]
    except Exception:
        return [False]
        
    try:
        sig_m = divisor_sigma(m)
        sig_n = divisor_sigma(n)
        q = (sig_m == sig_n) and (sig_n == m + n)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: sigma(m) != sigma(n) or sigma(n) != m + n"
]

N_HYP = 0
NEG_Q_INDEX = 0