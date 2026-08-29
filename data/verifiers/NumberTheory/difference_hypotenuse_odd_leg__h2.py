import math
import sympy

def conditions(witness) -> list[bool]:
    try:
        a, b, c = witness
        if not (isinstance(a, (int, sympy.Integer)) and 
                isinstance(b, (int, sympy.Integer)) and 
                isinstance(c, (int, sympy.Integer))):
            return [False, False, False]
        a = int(a)
        b = int(b)
        c = int(c)
    except Exception:
        return [False, False, False]

    try:
        h1 = (a > 0 and b > 0 and c > 0 and a**2 + b**2 == c**2)
    except Exception:
        h1 = False

    try:
        h2 = (b % 2 == 1)
    except Exception:
        h2 = False

    try:
        diff = c - b
        if diff <= 0:
            neg_q = True
        elif diff % 2 != 0:
            neg_q = True
        else:
            k_sq = diff // 2
            if k_sq == 0:
                neg_q = True
            else:
                k = math.isqrt(k_sq)
                neg_q = not (k * k == k_sq)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a, b, c are positive integers such that a^2 + b^2 = c^2",
    "H_2: b is an odd integer",
    "¬Q: There does not exist a positive integer k such that c - b = 2k^2"
]

N_HYP = 2
NEG_Q_INDEX = 2