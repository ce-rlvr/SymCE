import math
import sympy

def conditions(witness) -> list[bool]:
    try:
        d = sympy.sympify(witness)
        h1 = bool(d.is_integer is True and d > 0)
    except Exception:
        h1 = False

    try:
        d = sympy.sympify(witness)
        if d.is_integer is not True:
            neg_q = False
        else:
            d_int = int(d)
            if d_int < 0:
                neg_q = True
            elif d_int == 0:
                neg_q = False
            else:
                root = math.isqrt(d_int)
                neg_q = bool(root * root == d_int)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: d is a positive integer",
    "¬Q: The Diophantine equation x^2 - dy^2 = 1 does not have infinitely many solutions in positive integers"
]

N_HYP = 1
NEG_Q_INDEX = 1