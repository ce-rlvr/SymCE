import sympy
from sympy.ntheory import isprime

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False, False, False]
        p, a, b = witness
    except Exception:
        return [False, False, False]

    # H_1: Let p be a prime number.
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False

    # H_2: Let a and b be integers.
    try:
        h2 = isinstance(a, (int, sympy.Integer)) and isinstance(b, (int, sympy.Integer))
    except Exception:
        h2 = False

    # ¬Q: p does NOT divide a AND p does NOT divide b.
    try:
        neg_q = (a % p != 0) and (b % p != 0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: a and b are integers",
    "¬Q: p does not divide a and p does not divide b"
]

N_HYP = 2
NEG_Q_INDEX = 2