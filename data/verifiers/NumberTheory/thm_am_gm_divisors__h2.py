import sympy
from sympy.ntheory import divisor_sigma, divisor_count

def conditions(witness):
    try:
        n = witness
        h1 = isinstance(n, (int, sympy.Integer)) and n > 0
    except Exception:
        h1 = False

    try:
        n = witness
        if not (isinstance(n, (int, sympy.Integer)) and n > 0):
            neg_q = False
        else:
            sigma_n = divisor_sigma(n)
            tau_n = divisor_count(n)
            # The conclusion is sigma(n)/tau(n) >= sqrt(n)
            # The negated conclusion is sigma(n)/tau(n) < sqrt(n)
            # Since sigma_n, tau_n, and n are positive, this is equivalent to:
            neg_q = bool(sigma_n**2 < n * tau_n**2)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: sigma(n)/tau(n) < sqrt(n)"
]

N_HYP = 1
NEG_Q_INDEX = 1