import math
import sympy

def conditions(witness):
    try:
        if len(witness) != 2:
            return [False, False]
        a, b = witness
    except Exception:
        return [False, False]

    try:
        h1 = isinstance(a, (int, sympy.Integer)) and isinstance(b, (int, sympy.Integer))
    except Exception:
        h1 = False

    try:
        g = math.gcd(int(a + b), int(a - b))
        neg_q = g not in {1, 2}
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: a and b are integers",
    "¬Q: gcd(a+b, a-b) is not in {1, 2}"
]

N_HYP = 1
NEG_Q_INDEX = 1