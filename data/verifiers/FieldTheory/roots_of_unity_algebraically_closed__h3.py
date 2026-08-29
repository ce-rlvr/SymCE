import sympy
from sympy.ntheory import isprime

def conditions(witness):
    try:
        if isinstance(witness, dict):
            p = witness['p']
            n = witness['n']
        elif hasattr(witness, 'p') and hasattr(witness, 'n'):
            p = witness.p
            n = witness.n
        else:
            p, n = witness[:2]
    except Exception:
        return [False, False, False]

    try:
        h1 = (p == 0) or isprime(p)
    except Exception:
        h1 = False

    try:
        h2 = (int(n) == n) and (n > 0)
    except Exception:
        h2 = False

    try:
        neg_q = (p > 0) and (n % p == 0)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field of characteristic p >= 0 (p is 0 or prime)",
    "H_2: n is a positive integer",
    "¬Q: The polynomial x^n - 1 does not have exactly n distinct roots in K"
]

N_HYP = 2
NEG_Q_INDEX = 2