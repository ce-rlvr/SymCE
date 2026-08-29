import sympy
from sympy.ntheory import divisor_sigma

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            k = witness['k']
            n = witness['n']
        else:
            k, n = witness
    except Exception:
        return [False, False]

    try:
        k_val = int(k)
        h1 = (k_val == k) and (k_val > 1)
    except Exception:
        h1 = False

    try:
        n_val = int(n)
        k_val = int(k)
        if n_val == n and n_val > 0 and k_val == k and k_val > 0:
            neg_q = bool(divisor_sigma(k_val * n_val) <= 2 * k_val * n_val)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: k is an integer such that k > 1",
    "¬Q: sigma(kn) <= 2kn"
]

N_HYP = 1
NEG_Q_INDEX = 1