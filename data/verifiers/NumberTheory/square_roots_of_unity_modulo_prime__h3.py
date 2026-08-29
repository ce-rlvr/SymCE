import sympy
from sympy.ntheory import isprime

def conditions(witness) -> list[bool]:
    try:
        p, x = witness
    except Exception:
        return [False, False, False]

    # H_1: p is a prime
    try:
        h1 = isprime(p)
    except Exception:
        h1 = False

    # H_2: x is an integer
    try:
        h2 = (int(x) == x)
    except Exception:
        h2 = False

    # neg_Q: x is neither 1 nor -1 modulo p
    try:
        q = ((x % p) == (1 % p)) or ((x % p) == ((-1) % p))
        neg_q = not q
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: p is a prime",
    "H_2: x is an integer",
    "¬Q: x is neither 1 nor -1 modulo p"
]

N_HYP = 2
NEG_Q_INDEX = 2