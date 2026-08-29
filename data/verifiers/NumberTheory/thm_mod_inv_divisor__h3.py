import sympy
import math

def is_int(x):
    try:
        return int(x) == x and not isinstance(x, bool)
    except Exception:
        return False

def conditions(witness):
    try:
        witness = tuple(witness)
        if len(witness) != 3:
            return [False, False, False, False, False]
        n, a, d = witness
    except Exception:
        return [False, False, False, False, False]

    try:
        h1 = bool(is_int(n) and int(n) > 1)
    except Exception:
        h1 = False

    try:
        h2 = bool(is_int(a))
    except Exception:
        h2 = False

    try:
        h3 = bool(is_int(d) and int(d) > 1)
    except Exception:
        h3 = False

    try:
        h4 = bool(is_int(n) and is_int(d) and (int(n) % int(d) == 0))
    except Exception:
        h4 = False

    try:
        q = False
        if is_int(a) and is_int(d) and is_int(n):
            a_int = int(a)
            d_int = int(d)
            n_int = int(n)
            if math.gcd(a_int, d_int) == 1:
                try:
                    inv_n = sympy.mod_inverse(a_int, n_int)
                    if (inv_n * a_int) % d_int == 1:
                        q = True
                except Exception:
                    pass
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer strictly greater than 1",
    "H_2: a is an integer",
    "H_3: d is an integer strictly greater than 1",
    "H_4: d divides n",
    "¬Q: a is not invertible modulo d, or the modular inverse of a modulo n is not a modular inverse of a modulo d"
]

N_HYP = 4
NEG_Q_INDEX = 4