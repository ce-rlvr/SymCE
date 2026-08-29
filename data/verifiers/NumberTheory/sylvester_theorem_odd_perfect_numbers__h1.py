import sympy
from sympy.ntheory import divisor_sigma, primefactors

def conditions(witness):
    try:
        n = int(witness)
        if n <= 0:
            h1 = False
        else:
            h1 = bool(divisor_sigma(n) == 2 * n)
    except Exception:
        h1 = False

    try:
        n = int(witness)
        if n <= 0:
            neg_q = False
        else:
            neg_q = bool(len(primefactors(n)) < 3)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a perfect number (sigma(n) = 2n)",
    "¬Q: n has fewer than three distinct prime factors"
]

N_HYP = 1
NEG_Q_INDEX = 1