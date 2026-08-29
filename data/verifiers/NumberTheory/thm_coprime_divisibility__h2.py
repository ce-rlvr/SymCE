import math
import sympy

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False, False, False, False]
        a, b, c = witness
    except Exception:
        return [False, False, False, False]

    try:
        h1 = isinstance(a, (int, sympy.Integer)) and isinstance(b, (int, sympy.Integer)) and isinstance(c, (int, sympy.Integer))
        if h1:
            a, b, c = int(a), int(b), int(c)
    except Exception:
        h1 = False

    try:
        if not h1:
            h2 = False
        elif b == 0:
            h2 = (c == 0)
        else:
            h2 = (c % b == 0)
    except Exception:
        h2 = False

    try:
        if not h1:
            h3 = False
        else:
            h3 = (math.gcd(a, b) == 1)
    except Exception:
        h3 = False

    try:
        if not h1:
            neg_q = False
        else:
            ab = a * b
            if ab == 0:
                neg_q = (c != 0)
            else:
                neg_q = (c % ab != 0)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: a, b, and c are integers",
    "H_2: b divides c",
    "H_3: gcd(a, b) = 1",
    "¬Q: ab does not divide c"
]

N_HYP = 3
NEG_Q_INDEX = 3