import math
import sympy

# Top-level setup
# (No specific named objects needed for this number theory conjecture)

def conditions(witness) -> list[bool]:
    try:
        a, b, c = witness
    except Exception:
        return [False, False]

    try:
        h1 = (isinstance(a, (int, sympy.Integer)) and 
              isinstance(b, (int, sympy.Integer)) and 
              isinstance(c, (int, sympy.Integer)) and 
              a > 0 and b > 0 and c > 0)
    except Exception:
        h1 = False

    try:
        ab = int(a * b)
        if ab % 4 == 0:
            k2 = ab // 4
            if k2 >= 0:
                k = math.isqrt(k2)
                neg_q = (k * k == k2)
            else:
                neg_q = False
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a, b, and c are strictly positive integers",
    "¬Q: The area (a * b) / 2 is equal to twice the square of some integer"
]

N_HYP = 1
NEG_Q_INDEX = 1