import sympy
from sympy import gcd

def conditions(witness):
    try:
        if isinstance(witness, dict):
            a = witness['a']
            b = witness['b']
            c = witness['c']
        else:
            a, b, c = witness
    except Exception:
        return [False, False]

    try:
        h1 = bool(c > 0)
    except Exception:
        h1 = False

    try:
        lhs = gcd(c * a, c * b)
        rhs = c * gcd(a, b)
        diff = sympy.simplify(lhs - rhs)
        neg_q = bool(diff != 0)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: c > 0",
    "¬Q: gcd(c * a, c * b) != c * gcd(a, b)"
]

N_HYP = 1
NEG_Q_INDEX = 1