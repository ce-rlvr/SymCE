import sympy
from sympy.ntheory import divisor_sigma, divisor_count

def conditions(witness):
    try:
        if isinstance(witness, bool):
            h1 = False
        else:
            n = int(witness)
            h1 = (n == witness) and (n > 0)
    except Exception:
        h1 = False

    # H2 is definitional: sigma(n) is the sum of positive divisors of n.
    # It holds whenever n is a valid positive integer.
    h2 = h1

    try:
        if h1:
            sigma_n = divisor_sigma(n, 1)
            tau_n = divisor_count(n)
            neg_q = bool(sigma_n < n + tau_n - 1)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: sigma(n) is the sum of positive divisors of n",
    "¬Q: sigma(n) < n + tau(n) - 1"
]

N_HYP = 2
NEG_Q_INDEX = 2