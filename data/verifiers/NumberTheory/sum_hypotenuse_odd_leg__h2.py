import math
import sympy

def _is_int(x):
    return isinstance(x, (int, sympy.Integer)) and not isinstance(x, bool)

def conditions(witness):
    try:
        a, b, c = witness
        h1 = _is_int(a) and _is_int(b) and _is_int(c) and int(a) > 0 and int(b) > 0 and int(c) > 0
    except Exception:
        h1 = False

    try:
        a, b, c = witness
        if not (_is_int(a) and _is_int(b) and _is_int(c)):
            h2 = False
        else:
            h2 = math.gcd(math.gcd(int(a), int(b)), int(c)) == 1
    except Exception:
        h2 = False

    try:
        a, b, c = witness
        if not _is_int(a):
            h3 = False
        else:
            h3 = (int(a) % 2 == 1)
    except Exception:
        h3 = False

    try:
        a, b, c = witness
        if not (_is_int(a) and _is_int(c)):
            neg_q = False
        else:
            val = int(c) + int(a)
            if val < 2 or val % 2 != 0:
                is_2m2 = False
            else:
                k = val // 2
                root = math.isqrt(k)
                is_2m2 = (root * root == k) and (root > 0)
            neg_q = not is_2m2
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: a, b, and c are strictly positive integers",
    "H_2: \\gcd(a, b, c) = 1",
    "H_3: a is an odd integer",
    "¬Q: c + a is not of the form 2m^2 for any strictly positive integer m"
]

N_HYP = 3
NEG_Q_INDEX = 3