import sympy
import math

def conditions(witness):
    try:
        if isinstance(witness, (int, sympy.Integer)):
            n = int(witness)
            h1 = (n >= 1)
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        # The second hypothesis is definitional. 
        # If n is a valid positive integer, the definition applies.
        h2 = h1
    except Exception:
        h2 = False

    try:
        if h1:
            sigma_n = sympy.divisor_sigma(n, 1)
            tau_n = sympy.divisor_count(n)
            # We check sigma(n) < tau(n) * sqrt(n)
            # Squaring both sides to avoid floating-point inaccuracies:
            # sigma(n)^2 < tau(n)^2 * n
            neg_q = bool(sigma_n**2 < (tau_n**2) * n)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer such that n >= 1",
    "H_2: tau(n) is the number of positive divisors of n",
    "¬Q: sigma(n) < tau(n) * sqrt(n)"
]

N_HYP = 2
NEG_Q_INDEX = 2