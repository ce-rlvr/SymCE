import math
from sympy import sqrt, Rational
from sympy.ntheory import continued_fraction_iterator, continued_fraction_convergents

def is_int(v):
    try:
        return int(v) == v
    except Exception:
        return False

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False, False]
        d, x, y = witness
    except Exception:
        return [False, False, False]

    # H1: d is a positive integer that is not a perfect square
    try:
        h1 = False
        if is_int(d) and d > 0:
            d_int = int(d)
            root = math.isqrt(d_int)
            if root * root != d_int:
                h1 = True
    except Exception:
        h1 = False

    # H2: x^2 - dy^2 \in {-1, 1}
    try:
        h2 = False
        if is_int(x) and is_int(y) and is_int(d):
            x_int = int(x)
            y_int = int(y)
            d_int = int(d)
            val = x_int**2 - d_int * y_int**2
            if val in (-1, 1):
                h2 = True
    except Exception:
        h2 = False

    # neg_Q: x/y is NOT a convergent of sqrt(d)
    try:
        neg_q = False
        if is_int(x) and is_int(y) and is_int(d):
            x_int = int(x)
            y_int = int(y)
            d_int = int(d)
            
            if d_int <= 0:
                neg_q = True
            elif y_int == 0:
                neg_q = True
            else:
                target = Rational(x_int, y_int)
                if target < 0:
                    neg_q = True
                else:
                    iterator = continued_fraction_iterator(sqrt(d_int))
                    convergents = continued_fraction_convergents(iterator)
                    is_conv = False
                    for c in convergents:
                        if c == target:
                            is_conv = True
                            break
                        _, denom = c.as_numer_denom()
                        if denom > abs(y_int):
                            break
                    neg_q = not is_conv
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: d is a positive integer that is not a perfect square",
    "H_2: x^2 - dy^2 in {-1, 1}",
    "¬Q: x/y is not a convergent of the simple continued fraction expansion of sqrt(d)"
]

N_HYP = 2
NEG_Q_INDEX = 2