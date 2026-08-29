import math

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False, False, False, False]
        a, b, c = witness
        if int(a) != a or int(b) != b or int(c) != c:
            return [False, False, False, False]
        a, b, c = int(a), int(b), int(c)
    except Exception:
        return [False, False, False, False]

    try:
        h1_ok = (a**2 + b**2 == c**2)
    except Exception:
        h1_ok = False

    try:
        h2_ok = (math.gcd(math.gcd(a, b), c) == 1)
    except Exception:
        h2_ok = False

    try:
        h3_ok = (b % 2 == 0)
    except Exception:
        h3_ok = False

    try:
        diff = c - b
        if diff <= 0:
            neg_q_ok = True
        else:
            k = math.isqrt(diff)
            if k**2 == diff and k % 2 == 1 and k > 0:
                neg_q_ok = False
            else:
                neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: a^2 + b^2 = c^2",
    "H_2: gcd(a, b, c) = 1",
    "H_3: b is an even integer",
    "¬Q: c - b is not the square of an odd positive integer"
]

N_HYP = 3
NEG_Q_INDEX = 3