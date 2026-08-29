import math
import sympy

# Top-level setup
# No special bindings needed for number theory.

def conditions(witness) -> list[bool]:
    try:
        a, b, c = witness
    except Exception:
        return [False, False]

    try:
        a_int = int(a)
        b_int = int(b)
        c_int = int(c)
        h1 = (a_int == a and b_int == b and c_int == c and
              a_int > 0 and b_int > 0 and c_int > 0 and
              a_int**2 + b_int**2 == c_int**2)
    except Exception:
        h1 = False

    try:
        a_int = int(a)
        b_int = int(b)
        c_int = int(c)
        neg_q = math.gcd(c_int, a_int * b_int) != 1
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a, b, c are positive integers such that a^2 + b^2 = c^2",
    "¬Q: gcd(c, ab) != 1"
]

N_HYP = 1
NEG_Q_INDEX = 1