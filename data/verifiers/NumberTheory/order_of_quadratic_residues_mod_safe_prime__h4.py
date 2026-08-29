import sympy
from sympy.ntheory import isprime, legendre_symbol, n_order

def conditions(witness) -> list[bool]:
    try:
        q, p, a = witness
    except Exception:
        return [False] * 5
    
    try:
        h1 = bool(isprime(q) and q > 2)
    except Exception:
        h1 = False

    try:
        h2 = bool(isprime(p) and p == 2 * q + 1)
    except Exception:
        h2 = False

    try:
        if p > 0:
            h3 = bool(legendre_symbol(a, p) == 1 or a % p == 0)
        else:
            h3 = False
    except Exception:
        h3 = False

    try:
        h4 = bool(a % p != 0)
    except Exception:
        h4 = False

    try:
        if sympy.gcd(a, p) == 1:
            neg_q = bool(n_order(a, p) != q)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: q is a prime strictly greater than 2",
    "H_2: p is a prime such that p = 2q + 1",
    "H_3: a is a quadratic residue modulo p",
    "H_4: a is not congruent to 0 mod p",
    "¬Q: The order of a modulo p is not exactly q"
]

N_HYP = 4
NEG_Q_INDEX = 4