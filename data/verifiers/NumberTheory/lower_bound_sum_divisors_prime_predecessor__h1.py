import sympy
from sympy.ntheory import divisor_sigma

def conditions(witness):
    try:
        p = int(witness)
        neg_q = bool(divisor_sigma(p - 1) < p)
    except Exception:
        neg_q = False
    return [neg_q]

CONDITION_LABELS = ["¬Q: sigma(p-1) < p"]
N_HYP = 0
NEG_Q_INDEX = 0