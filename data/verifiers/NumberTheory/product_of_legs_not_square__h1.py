import math
import sympy
from sympy import Integer, Rational

def conditions(witness) -> list[bool]:
    try:
        a, b, c = witness
        a = int(a)
        b = int(b)
        c = int(c)
    except Exception:
        return [False, False]

    try:
        h1 = (math.gcd(math.gcd(a, b), c) == 1)
    except Exception:
        h1 = False

    try:
        prod = a * b
        if prod < 0:
            neg_q = False
        else:
            root = math.isqrt(prod)
            neg_q = (root * root == prod)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: gcd(a, b, c) = 1",
    "¬Q: ab is the square of an integer"
]

N_HYP = 1
NEG_Q_INDEX = 1