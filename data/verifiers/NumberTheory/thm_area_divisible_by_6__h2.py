import sympy
import math

CONDITION_LABELS = [
    "H_1: a, b, and c are positive integers",
    "¬Q: The area of the right triangle formed by a, b, and c is not an integer multiple of 6"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if len(witness) != 3:
            h1 = False
        else:
            a, b, c = witness
            h1 = (int(a) == a) and (int(b) == b) and (int(c) == c) and (a > 0) and (b > 0) and (c > 0)
    except Exception:
        h1 = False

    try:
        a, b, c = witness
        # In the context of Pythagorean triples (a, b, c), a and b are the legs.
        # The area of the right triangle with legs a and b is a * b / 2.
        area_double = a * b
        if area_double % 2 != 0:
            # Area is not an integer
            neg_q = True
        else:
            area = area_double // 2
            neg_q = (area % 6 != 0)
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]