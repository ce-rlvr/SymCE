import sympy
from sympy.ntheory import isprime

def conditions(witness) -> list[bool]:
    try:
        p, a = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False

    try:
        h2 = isinstance(a, (int, sympy.Integer))
    except Exception:
        h2 = False

    try:
        neg_q = bool((a**2 - a + 1) % p != 0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: a is an integer",
    "¬Q: a^2 - a + 1 is not congruent to 0 mod p"
]

N_HYP = 2
NEG_Q_INDEX = 2