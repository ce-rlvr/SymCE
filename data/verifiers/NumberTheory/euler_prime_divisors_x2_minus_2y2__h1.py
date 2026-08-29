import sympy
import math

def is_int(val):
    return isinstance(val, (int, sympy.Integer)) and not isinstance(val, bool)

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False, False, False]
        x, y, p = witness
    except Exception:
        return [False, False, False, False]

    # H_1: x and y are integers
    try:
        h1 = is_int(x) and is_int(y)
    except Exception:
        h1 = False

    # H_2: \gcd(x, y) = 1
    try:
        h2 = h1 and math.gcd(int(x), int(y)) == 1
    except Exception:
        h2 = False

    # H_3: p divides x^2 - 2y^2
    try:
        h3 = is_int(p) and int(p) != 0 and (int(x)**2 - 2*int(y)**2) % int(p) == 0
    except Exception:
        h3 = False

    # ¬Q: p is not congruent to 1 or 7 mod 8
    try:
        neg_q = is_int(p) and (int(p) % 8) not in (1, 7)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: x and y are integers",
    "H_2: gcd(x, y) = 1",
    "H_3: p divides x^2 - 2y^2",
    "¬Q: p is not congruent to 1 or 7 mod 8"
]

N_HYP = 3
NEG_Q_INDEX = 3