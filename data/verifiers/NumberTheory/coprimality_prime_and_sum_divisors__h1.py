import sympy
import sympy.ntheory
import math

def conditions(witness):
    try:
        p = int(witness)
        if p < 1:
            neg_q = False
        else:
            sigma_p = sympy.ntheory.divisor_sigma(p)
            neg_q = bool(math.gcd(p, int(sigma_p)) != 1)
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: gcd(p, sigma(p)) != 1"
]

N_HYP = 0
NEG_Q_INDEX = 0