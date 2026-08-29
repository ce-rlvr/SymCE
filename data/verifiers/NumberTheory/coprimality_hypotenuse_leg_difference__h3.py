import math
import sympy

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the given witness.
    The witness should be a tuple or list of three integers (a, b, c).
    """
    try:
        a, b, c = witness
    except Exception:
        return [False, False, False]

    # H_1: a, b, and c are strictly positive integers
    try:
        h1 = (int(a) == a) and (int(b) == b) and (int(c) == c) and (a > 0) and (b > 0) and (c > 0)
    except Exception:
        h1 = False

    # H_2: a^2 + b^2 = c^2
    try:
        h2 = (a**2 + b**2 == c**2)
    except Exception:
        h2 = False

    # ¬Q: The greatest common divisor of c and |a-b| is not 1
    try:
        neg_q = math.gcd(int(c), int(abs(a - b))) != 1
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: a, b, and c are strictly positive integers",
    "H_2: a^2 + b^2 = c^2",
    "¬Q: The greatest common divisor of c and |a-b| is not 1"
]

N_HYP = 2
NEG_Q_INDEX = 2