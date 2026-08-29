import sympy
from sympy.ntheory import isprime, legendre_symbol

# Top-level setup
# No named bindings needed for this number theory conjecture.

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            p = witness['p']
            a = witness['a']
            b = witness['b']
        else:
            p, a, b = witness
            
        p = int(p)
        a = int(a)
        b = int(b)
    except Exception:
        return [False, False, False]

    try:
        h1 = bool(isprime(p) and p % 2 != 0)
    except Exception:
        h1 = False

    try:
        h2 = bool(legendre_symbol(a, p) == -1)
    except Exception:
        h2 = False

    try:
        neg_q = bool(legendre_symbol(a * b, p) != 1)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is an odd prime",
    "H_2: (a/p) = -1",
    "¬Q: (ab/p) != 1"
]

N_HYP = 2
NEG_Q_INDEX = 2