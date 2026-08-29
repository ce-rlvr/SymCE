import math
import sympy

def conditions(witness):
    try:
        a, b, q, r = witness
    except Exception:
        return [False, False]

    try:
        h1 = all(isinstance(x, (int, sympy.Integer)) for x in (a, b, q, r))
    except Exception:
        h1 = False

    try:
        neg_q = math.gcd(int(a), int(b)) != math.gcd(int(b), int(r))
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a, b, q, and r are integers",
    "¬Q: gcd(a, b) != gcd(b, r)"
]

N_HYP = 1
NEG_Q_INDEX = 1