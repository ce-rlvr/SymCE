import sympy
from sympy.ntheory import totient

def conditions(witness) -> list[bool]:
    try:
        m, n = witness
    except Exception:
        return [False, False]

    try:
        h1 = isinstance(m, int) and m > 0
    except Exception:
        h1 = False

    try:
        lhs = totient(m * n) * totient(sympy.gcd(m, n))
        rhs = totient(m) * totient(n) * sympy.gcd(m, n)
        neg_q = bool(lhs != rhs)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: m is a positive integer",
    "¬Q: phi(mn)phi(gcd(m, n)) != phi(m)phi(n)gcd(m, n)"
]

N_HYP = 1
NEG_Q_INDEX = 1