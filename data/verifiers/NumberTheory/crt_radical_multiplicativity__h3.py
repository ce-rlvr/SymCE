import sympy
from sympy.ntheory import factorint

def rad(n):
    if n <= 0:
        raise ValueError("n must be positive")
    factors = factorint(n)
    res = 1
    for p in factors:
        res *= p
    return res

def conditions(witness) -> list[bool]:
    try:
        a, b = witness
    except Exception:
        return [False, False]

    try:
        h1_ok = bool(isinstance(a, (int, sympy.Integer)) and isinstance(b, (int, sympy.Integer)) and a > 0 and b > 0)
    except Exception:
        h1_ok = False

    try:
        if h1_ok:
            neg_Q_ok = bool(rad(a * b) != rad(a) * rad(b))
        else:
            neg_Q_ok = False
    except Exception:
        neg_Q_ok = False

    return [h1_ok, neg_Q_ok]

CONDITION_LABELS = [
    "H_1: a and b are positive integers",
    "¬Q: rad(ab) != rad(a)rad(b)"
]

N_HYP = 1
NEG_Q_INDEX = 1