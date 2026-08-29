import math
import sympy

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 4:
            return [False, False, False, False]
        a, b, c, m = witness
    except Exception:
        return [False, False, False, False]

    try:
        h1 = all(isinstance(x, (int, sympy.Integer)) and not isinstance(x, bool) for x in (a, b, c, m))
    except Exception:
        h1 = False

    try:
        h2 = bool(m > 0)
    except Exception:
        h2 = False

    try:
        h3 = bool(math.gcd(int(c), int(m)) == 1)
    except Exception:
        h3 = False

    try:
        neg_q = bool((a - b) % m != 0)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: a, b, c, and m are integers",
    "H_2: m > 0",
    "H_3: gcd(c, m) = 1",
    "¬Q: a is not congruent to b modulo m"
]

N_HYP = 3
NEG_Q_INDEX = 3