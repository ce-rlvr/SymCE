import sympy
from sympy.ntheory import isprime

def conditions(witness):
    try:
        if isinstance(witness, dict):
            p = witness.get('p')
            n = witness.get('n')
            k = witness.get('k')
        else:
            p, n, k = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False

    try:
        h2 = isinstance(n, int) and n > 0
    except Exception:
        h2 = False

    try:
        if not isinstance(k, int):
            neg_q = False
        else:
            lhs = sympy.binomial(p**n - 1, k)
            rhs = 1 if k % 2 == 0 else -1
            neg_q = (lhs % p) != (rhs % p)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: n is a positive integer",
    "¬Q: binomial(p**n - 1, k) is not congruent to (-1)**k mod p"
]

N_HYP = 2
NEG_Q_INDEX = 2