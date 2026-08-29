import math
import sympy
from sympy import Integer, Rational

# Top-level setup
# No specific named bindings needed for this number theory conjecture.

def conditions(witness) -> list[bool]:
    try:
        # Witness is expected to be a tuple or list of three integers: (a, b, c)
        if len(witness) != 3:
            return [False, False, False, False]
        a, b, c = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: a, b, and c are strictly positive integers
    try:
        a_int = int(a)
        b_int = int(b)
        c_int = int(c)
        h1 = (a_int == a) and (b_int == b) and (c_int == c) and \
             (not isinstance(a, bool)) and (not isinstance(b, bool)) and (not isinstance(c, bool)) and \
             (a_int > 0) and (b_int > 0) and (c_int > 0)
    except Exception:
        h1 = False

    # H_2: a^2 + b^2 = c^2
    try:
        h2 = bool(a**2 + b**2 == c**2)
    except Exception:
        h2 = False

    # H_3: b is an even integer
    try:
        h3 = bool(b % 2 == 0)
    except Exception:
        h3 = False

    # ¬Q: The greatest common divisor of c-b and c+b is not 1
    try:
        neg_q = bool(math.gcd(int(c - b), int(c + b)) != 1)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: a, b, and c are strictly positive integers",
    "H_2: a^2 + b^2 = c^2",
    "H_3: b is an even integer",
    "¬Q: The greatest common divisor of c-b and c+b is not 1"
]

N_HYP = 3
NEG_Q_INDEX = 3