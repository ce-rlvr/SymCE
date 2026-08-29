import sympy
from sympy import isprime

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            x = witness['x']
            p = witness['p']
        else:
            x, p = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = isinstance(x, (int, sympy.Integer)) or (hasattr(x, 'is_integer') and x.is_integer)
        h1 = bool(h1)
    except Exception:
        h1 = False

    try:
        h2 = isinstance(p, (int, sympy.Integer)) and isprime(p) and p % 2 != 0
        h2 = bool(h2)
    except Exception:
        h2 = False

    try:
        neg_q = bool(p % 4 != 1)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: x is an integer",
    "H_2: p is an odd prime",
    "¬Q: p is not congruent to 1 modulo 4"
]

N_HYP = 2
NEG_Q_INDEX = 2