import math
import sympy

CONDITION_LABELS = [
    "H_1: xy = z^2",
    "H_2: gcd(x,y) = 1",
    "¬Q: x and y are not both squares of positive integers"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            x = int(witness['x'])
            y = int(witness['y'])
            z = int(witness['z'])
        else:
            x, y, z = witness
            x = int(x)
            y = int(y)
            z = int(z)
    except Exception:
        return [False, False, False]

    try:
        h1_ok = (x * y == z ** 2)
    except Exception:
        h1_ok = False

    try:
        h2_ok = (math.gcd(x, y) == 1)
    except Exception:
        h2_ok = False

    try:
        def is_pos_sq(n):
            if n <= 0:
                return False
            r = math.isqrt(n)
            return r * r == n
        
        neg_q_ok = not (is_pos_sq(x) and is_pos_sq(y))
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]