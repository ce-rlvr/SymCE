import sympy
from sympy.ntheory import isprime, divisor_sigma

def conditions(witness):
    try:
        p = int(witness)
        h1 = bool(isprime(p))
    except Exception:
        h1 = False

    try:
        p = int(witness)
        sigma_val = divisor_sigma(p * (p + 2))
        expected = p**2 + 4*p + 3
        neg_q = bool(sigma_val != expected)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "¬Q: sigma(p(p+2)) != p^2 + 4p + 3"
]

N_HYP = 1
NEG_Q_INDEX = 1