import math
import sympy

def conditions(witness) -> list[bool]:
    try:
        a, b = witness
    except Exception:
        return [False, False]

    try:
        h1 = isinstance(a, (int, sympy.Integer)) and isinstance(b, (int, sympy.Integer))
    except Exception:
        h1 = False

    try:
        a_int = int(a)
        b_int = int(b)
        val = math.gcd(a_int + b_int, a_int**2 - a_int*b_int + b_int**2)
        neg_q = val not in {1, 3}
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a and b are integers",
    "¬Q: gcd(a+b, a^2 - ab + b^2) is not in {1, 3}"
]

N_HYP = 1
NEG_Q_INDEX = 1