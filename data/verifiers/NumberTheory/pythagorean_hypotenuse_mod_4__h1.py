import math
import sympy

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False, False, False]
        a, b, c = witness
        if int(a) != a or int(b) != b or int(c) != c:
            return [False, False, False]
        a, b, c = int(a), int(b), int(c)
    except Exception:
        return [False, False, False]

    try:
        h1_ok = bool(a**2 + b**2 == c**2)
    except Exception:
        h1_ok = False

    try:
        h2_ok = bool(math.gcd(math.gcd(a, b), c) == 1)
    except Exception:
        h2_ok = False

    try:
        neg_q_ok = bool(c % 4 != 1)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: a^2 + b^2 = c^2",
    "H_2: gcd(a, b, c) = 1",
    "¬Q: c is not congruent to 1 mod 4"
]

N_HYP = 2
NEG_Q_INDEX = 2