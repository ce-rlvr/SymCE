import math
import sympy

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False, False]
        a, b, c = witness
    except Exception:
        return [False, False, False]

    # H_1: a, b, and c are strictly positive integers
    try:
        h1 = (int(a) == a) and (int(b) == b) and (int(c) == c) and (a > 0) and (b > 0) and (c > 0)
        if isinstance(a, bool) or isinstance(b, bool) or isinstance(c, bool):
            h1 = False
    except Exception:
        h1 = False

    # H_2: \gcd(a, b, c) = 1
    try:
        a_int, b_int, c_int = int(a), int(b), int(c)
        h2 = math.gcd(math.gcd(a_int, b_int), c_int) == 1
    except Exception:
        h2 = False

    # ¬Q: The product abc is a perfect square
    try:
        a_int, b_int, c_int = int(a), int(b), int(c)
        prod = a_int * b_int * c_int
        if prod < 0:
            neg_q = False
        else:
            root = math.isqrt(prod)
            neg_q = (root * root == prod)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a, b, and c are strictly positive integers",
    "H_2: gcd(a, b, c) = 1",
    "¬Q: The product abc is a perfect square"
]

N_HYP = 2
NEG_Q_INDEX = 2