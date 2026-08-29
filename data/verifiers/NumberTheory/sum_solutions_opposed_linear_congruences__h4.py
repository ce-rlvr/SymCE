import math
import sympy
from sympy import Rational, Integer

def is_int(x):
    try:
        return int(x) == x and not isinstance(x, bool)
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            a = witness['a']
            b = witness['b']
            m = witness['m']
            x_1 = witness['x_1']
            x_2 = witness['x_2']
        else:
            a, b, m, x_1, x_2 = witness
    except Exception:
        return [False, False, False, False]

    try:
        h1 = is_int(a) and is_int(b) and is_int(m) and int(m) > 0
    except Exception:
        h1 = False

    try:
        h2 = math.gcd(int(a), int(m)) == 1
    except Exception:
        h2 = False

    try:
        h3 = is_int(x_1) and (int(a) * int(x_1)) % int(m) == int(b) % int(m)
    except Exception:
        h3 = False

    try:
        neg_q = is_int(x_2) and (int(x_1) + int(x_2)) % int(m) != 0
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: a, b, m are integers with m > 0",
    "H_2: gcd(a, m) == 1",
    "H_3: x_1 is an integer such that a*x_1 == b (mod m)",
    "¬Q: x_1 + x_2 != 0 (mod m)"
]

N_HYP = 3
NEG_Q_INDEX = 3