import sympy
from sympy.ntheory import isprime, legendre_symbol

# Top-level setup
# No specific named bindings required for this number theory conjecture.

def conditions(witness) -> list[bool]:
    try:
        p, a = witness
    except Exception:
        return [False, False, False, False]

    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False

    try:
        h2 = isinstance(a, int) or isinstance(a, sympy.Integer)
    except Exception:
        h2 = False

    try:
        h3 = (a % p != 0)
    except Exception:
        h3 = False

    try:
        l1 = legendre_symbol(a, p)
        l2 = legendre_symbol(-a, p)
        exactly_one = ((l1 == 1 and l2 != 1) or (l1 != 1 and l2 == 1))
        neg_q = not exactly_one
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS: list[str] = [
    "H_1: p is a prime number",
    "H_2: a is an integer",
    "H_3: p does not divide a",
    "¬Q: It is not the case that exactly one of (a/p) or (-a/p) is equal to 1"
]

N_HYP: int = 3
NEG_Q_INDEX: int = 3