import math
import sympy

def conditions(witness) -> list[bool]:
    try:
        a, b, c = witness
    except Exception:
        return [False, False, False, False]
    
    try:
        h1 = (isinstance(a, (int, sympy.Integer)) and 
              isinstance(b, (int, sympy.Integer)) and 
              isinstance(c, (int, sympy.Integer)) and 
              a > 0 and b > 0 and c > 0)
    except Exception:
        h1 = False

    try:
        h2 = math.gcd(math.gcd(int(a), int(b)), int(c)) == 1
    except Exception:
        h2 = False

    try:
        h3 = int(b) % 2 == 0
    except Exception:
        h3 = False

    try:
        val = int(c) + int(b)
        if val <= 0:
            neg_q = True
        else:
            s = math.isqrt(val)
            is_odd_square = (s * s == val) and (s % 2 == 1)
            neg_q = not is_odd_square
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: a, b, and c are positive integers",
    "H_2: gcd(a, b, c) = 1",
    "H_3: b is an even integer",
    "¬Q: c + b is not the square of an odd positive integer"
]

N_HYP = 3
NEG_Q_INDEX = 3