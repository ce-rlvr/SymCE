import math
import sympy

def conditions(witness) -> list[bool]:
    try:
        a, b = witness
    except Exception:
        return [False, False]

    try:
        h1 = bool(math.gcd(int(a), int(b)) == 1)
    except Exception:
        h1 = False

    try:
        neg_q = bool(math.lcm(int(a), int(b)) != int(a) * int(b))
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: gcd(a, b) == 1",
    "¬Q: lcm(a, b) != ab"
]

N_HYP = 1
NEG_Q_INDEX = 1