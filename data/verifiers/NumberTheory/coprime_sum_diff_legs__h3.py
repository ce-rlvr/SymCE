import math

def conditions(witness):
    try:
        # Witness is expected to be a tuple or list of three integers (a, b, c)
        if len(witness) != 3:
            return [False, False, False]
        a, b, c = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = (int(a) == a) and (int(b) == b) and (int(c) == c) and (a > 0) and (b > 0) and (c > 0)
    except Exception:
        h1 = False

    try:
        h2 = (a**2 + b**2 == c**2)
    except Exception:
        h2 = False

    try:
        neg_q = math.gcd(int(a + b), int(abs(a - b))) != 1
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: a, b, and c are strictly positive integers",
    "H_2: a^2 + b^2 = c^2",
    "¬Q: gcd(a + b, |a - b|) != 1"
]

N_HYP = 2
NEG_Q_INDEX = 2