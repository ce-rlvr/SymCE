import sympy
import math

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False, False, False]
        x, y, z = witness
    except Exception:
        return [False, False, False, False]

    try:
        h1 = (isinstance(x, (int, sympy.Integer)) and 
              isinstance(y, (int, sympy.Integer)) and 
              isinstance(z, (int, sympy.Integer)) and 
              x > 0 and y > 0 and z > 0)
    except Exception:
        h1 = False

    try:
        h2 = bool(x < y and y < z)
    except Exception:
        h2 = False

    try:
        h3 = bool(x**2 + y**2 == z**2)
    except Exception:
        h3 = False

    try:
        is_345_multiple = False
        if x % 3 == 0:
            k = x // 3
            if k > 0 and y == 4 * k and z == 5 * k:
                is_345_multiple = True
        neg_q = not is_345_multiple
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: x, y, z are positive integers",
    "H_2: x < y < z",
    "H_3: x^2 + y^2 = z^2",
    "¬Q: There does not exist a positive integer k such that x=3k, y=4k, z=5k"
]

N_HYP = 3
NEG_Q_INDEX = 3