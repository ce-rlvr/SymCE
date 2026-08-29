import sympy
from sympy.ntheory import isprime, n_order

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 2:
            return [False, False, False]
        a, p = witness
    except Exception:
        return [False, False, False]

    try:
        a = int(a)
        p = int(p)
    except Exception:
        return [False, False, False]

    # H1: p is an odd prime
    try:
        h1 = bool(isprime(p) and p > 2)
    except Exception:
        h1 = False

    # H2: a is not divisible by p
    try:
        if p != 0:
            h2 = bool(a % p != 0)
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: The order of a modulo p does NOT divide (p-1)/2
    try:
        if h1 and h2:
            order = n_order(a, p)
            neg_q = bool(((p - 1) // 2) % order != 0)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is an odd prime",
    "H_2: a is not divisible by p",
    "¬Q: The order of a modulo p does not divide (p-1)/2"
]

N_HYP = 2
NEG_Q_INDEX = 2