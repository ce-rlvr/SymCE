import math
import sympy

# Top-level setup
# (No named bindings needed for this number theory conjecture)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False, False, False]
        a, b, c = witness
    except Exception:
        return [False, False, False]

    try:
        a_int = int(a)
        b_int = int(b)
        c_int = int(c)
        h1 = (a_int == a) and (b_int == b) and (c_int == c) and (a_int > 0) and (b_int > 0) and (c_int > 0)
    except Exception:
        h1 = False

    try:
        h2 = bool(a**2 + b**2 == c**2)
    except Exception:
        h2 = False

    try:
        def is_square(n):
            n_int = int(n)
            if n_int < 0:
                return False
            r = math.isqrt(n_int)
            return r * r == n_int
        
        squares_count = sum(1 for x in (a, b, c) if is_square(x))
        neg_q = bool(squares_count >= 2)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a, b, and c are strictly positive integers",
    "H_2: a^2 + b^2 = c^2",
    "¬Q: At least two of the integers a, b, c are perfect squares"
]

N_HYP = 2
NEG_Q_INDEX = 2