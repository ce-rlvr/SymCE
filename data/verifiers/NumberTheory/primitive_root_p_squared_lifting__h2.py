import sympy
from sympy.ntheory import isprime, is_primitive_root

def conditions(witness):
    try:
        if isinstance(witness, dict):
            p = witness.get('p')
            k = witness.get('k')
            g = witness.get('g')
        else:
            p, k, g = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = bool(int(p) == p and isprime(p) and p % 2 != 0)
    except Exception:
        h1 = False

    try:
        h2 = bool(int(k) == k and k >= 2)
    except Exception:
        h2 = False

    try:
        neg_q = not bool(is_primitive_root(g, p**k))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is an odd prime number",
    "H_2: k is an integer greater than or equal to 2",
    "¬Q: g is not a primitive root modulo p^k"
]

N_HYP = 2
NEG_Q_INDEX = 2