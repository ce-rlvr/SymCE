import sympy
from sympy.ntheory import divisor_sigma

def conditions(witness) -> list[bool]:
    try:
        m, n = witness
        if int(m) < 1 or int(n) < 1:
            return [False]
        neg_q = bool(divisor_sigma(m * n) > divisor_sigma(m) * divisor_sigma(n))
    except Exception:
        neg_q = False
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: sigma(mn) > sigma(m)sigma(n)"
]

N_HYP = 0
NEG_Q_INDEX = 0