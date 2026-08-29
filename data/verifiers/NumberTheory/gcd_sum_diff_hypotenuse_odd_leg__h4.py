import math
import sympy

def conditions(witness):
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
        h2 = (a**2 + b**2 == c**2)
    except Exception:
        h2 = False

    try:
        h3 = (math.gcd(math.gcd(int(a), int(b)), int(c)) == 1)
    except Exception:
        h3 = False

    try:
        neg_q = (math.gcd(int(c - a), int(c + a)) != 2)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: a, b, and c are strictly positive integers",
    "H_2: a^2 + b^2 = c^2",
    "H_3: gcd(a, b, c) = 1",
    "¬Q: gcd(c - a, c + a) != 2"
]

N_HYP = 3
NEG_Q_INDEX = 3