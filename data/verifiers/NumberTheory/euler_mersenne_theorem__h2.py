import sympy
from sympy.ntheory import isprime

def conditions(witness) -> list[bool]:
    try:
        p = int(witness)
        h1 = bool(isprime(p))
    except Exception:
        h1 = False

    try:
        p = int(witness)
        q = 2 * p + 1
        h2 = bool(isprime(q))
    except Exception:
        h2 = False

    try:
        p = int(witness)
        q = 2 * p + 1
        # neg_Q: q does NOT divide 2^p - 1
        # We check if 2^p ≢ 1 (mod q)
        neg_q = bool(pow(2, p, q) != 1)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: q = 2p + 1 is a prime number",
    "¬Q: q does not divide 2^p - 1"
]

N_HYP = 2
NEG_Q_INDEX = 2