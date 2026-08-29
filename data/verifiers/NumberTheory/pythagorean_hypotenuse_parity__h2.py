import math

def conditions(witness):
    try:
        w = tuple(witness)
        if len(w) != 3:
            return [False, False, False]
        a, b, c = w
    except Exception:
        return [False, False, False]

    try:
        a_int = int(a)
        b_int = int(b)
        c_int = int(c)
        h1 = (a_int == a) and (b_int == b) and (c_int == c) and (a_int > 0) and (b_int > 0) and (c_int > 0)
    except Exception:
        h1 = False

    try:
        h2 = math.gcd(math.gcd(int(a), int(b)), int(c)) == 1
    except Exception:
        h2 = False

    try:
        neg_q = (int(c) % 2 == 0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a, b, and c are positive integers",
    "H_2: gcd(a, b, c) = 1",
    "¬Q: c is even"
]

N_HYP = 2
NEG_Q_INDEX = 2