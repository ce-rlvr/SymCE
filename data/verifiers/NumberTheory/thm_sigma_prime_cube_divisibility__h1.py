import sympy
from sympy.ntheory import divisor_sigma

def conditions(witness) -> list[bool]:
    try:
        p = int(witness)
        if p < 1 or p > 10**6:
            neg_q = False
        else:
            sig_p = divisor_sigma(p)
            sig_p3 = divisor_sigma(p**3)
            neg_q = bool(sig_p3 % sig_p != 0)
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: sigma(p^3) is not divisible by sigma(p)"
]

N_HYP = 0
NEG_Q_INDEX = 0