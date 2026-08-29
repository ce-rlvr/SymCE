import math
from sympy import isprime

def conditions(witness):
    try:
        p = int(witness)
        h1 = bool(isprime(p) and p % 2 != 0)
    except Exception:
        h1 = False

    try:
        p = int(witness)
        has_solution = False
        if p >= 0:
            max_y = int(math.isqrt(p // 2))
            for y in range(max_y + 1):
                rem = p - 2 * y**2
                if rem >= 0:
                    x = math.isqrt(rem)
                    if x**2 == rem:
                        has_solution = True
                        break
        neg_q = not has_solution
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p is an odd prime number",
    "¬Q: There do not exist integers x and y such that p = x^2 + 2y^2"
]

N_HYP = 1
NEG_Q_INDEX = 1