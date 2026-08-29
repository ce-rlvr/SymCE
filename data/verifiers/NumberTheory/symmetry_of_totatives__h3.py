import math
import sympy

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: k is a positive integer",
    "H_3: gcd(k, n) = 1",
    "¬Q: gcd(n - k, n) != 1"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, dict):
            n = witness['n']
            k = witness['k']
        else:
            n, k = witness
    except Exception:
        return [False, False, False, False]

    try:
        h1 = isinstance(n, (int, sympy.Integer)) and n > 0
    except Exception:
        h1 = False

    try:
        h2 = isinstance(k, (int, sympy.Integer)) and k > 0
    except Exception:
        h2 = False

    try:
        h3 = math.gcd(int(k), int(n)) == 1
    except Exception:
        h3 = False

    try:
        neg_q = math.gcd(int(n - k), int(n)) != 1
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]