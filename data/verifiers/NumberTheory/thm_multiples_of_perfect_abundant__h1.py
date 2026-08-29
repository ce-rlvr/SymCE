import sympy
from sympy.ntheory import divisor_sigma

def conditions(witness):
    try:
        if isinstance(witness, dict):
            n = witness['n']
            k = witness['k']
        else:
            n, k = witness
    except Exception:
        return [False, False]

    try:
        h1 = (int(k) == k) and (k > 1)
    except Exception:
        h1 = False

    try:
        if (int(n) == n) and (int(k) == k) and (n > 0) and (k > 0):
            val = int(n * k)
            neg_q = bool(divisor_sigma(val) <= 2 * val)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: k is an integer strictly greater than 1",
    "¬Q: sigma(nk) <= 2nk"
]

N_HYP = 1
NEG_Q_INDEX = 1