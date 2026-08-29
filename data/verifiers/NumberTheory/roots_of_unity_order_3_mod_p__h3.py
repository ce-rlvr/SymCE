import sympy
from sympy import isprime

# Top-level setup
# (No named bindings needed for this domain)

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
        h2 = isinstance(a, (int, sympy.Integer)) or (hasattr(a, 'is_integer') and a.is_integer)
    except Exception:
        h2 = False

    try:
        neg_q = ((int(a)**2 + int(a) + 1) % int(p)) != 0
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime",
    "H_2: a is an integer",
    "¬Q: a^2 + a + 1 is not congruent to 0 mod p"
]

N_HYP = 2
NEG_Q_INDEX = 2