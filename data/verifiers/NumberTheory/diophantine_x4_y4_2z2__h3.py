import math
from sympy import Integer, Rational

# Top-level setup
# No specific named objects required for this number theory conjecture.

def conditions(witness):
    try:
        w = list(witness)
        if len(w) != 3:
            return [False, False, False]
        x, y, z = w
    except Exception:
        return [False, False, False]

    try:
        x_int = int(x)
        y_int = int(y)
        z_int = int(z)
        h1 = (not isinstance(x, bool) and not isinstance(y, bool) and not isinstance(z, bool) and
              x_int == x and y_int == y and z_int == z and 
              x_int > 0 and y_int > 0 and z_int > 0)
    except Exception:
        h1 = False

    try:
        h2 = math.gcd(int(x), int(y)) == 1
    except Exception:
        h2 = False

    try:
        neg_q = not (int(x) == 1 and int(y) == 1 and int(z) == 1)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: x, y, and z are positive integers",
    "H_2: gcd(x, y) = 1",
    "¬Q: x, y, and z are not all 1"
]

N_HYP = 2
NEG_Q_INDEX = 2