import sympy
from sympy.ntheory import totient, divisor_sigma, divisors

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, bool):
            return [False, False, False]
        n = int(witness)
        if n != witness:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        h1 = (n > 1)
    except Exception:
        h1 = False

    try:
        if n > 0:
            h2 = bool(divisor_sigma(n) == sum(divisors(n)))
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        neg_q = bool(totient(n) * divisor_sigma(n) >= n**2)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    r"H_1: n is an integer strictly greater than 1",
    r"H_2: \sigma(n) is the sum of the positive divisors of n",
    r"¬Q: \phi(n) \sigma(n) >= n^2"
]

N_HYP = 2
NEG_Q_INDEX = 2