import math
from sympy import integer_nthroot

def conditions(witness) -> list[bool]:
    # H_1: (a, b, c) is a primitive Pythagorean triple
    try:
        a, b, c = witness
        a = int(a)
        b = int(b)
        c = int(c)
        h1 = (a > 0 and b > 0 and c > 0 and 
              a**2 + b**2 == c**2 and 
              math.gcd(a, math.gcd(b, c)) == 1)
    except Exception:
        h1 = False

    # neg_Q: There exists an integer k such that A = k^3
    try:
        a, b, c = witness
        a = int(a)
        b = int(b)
        A = (a * b) // 2
        if (a * b) % 2 == 0:
            abs_A = abs(A)
            root, exact = integer_nthroot(abs_A, 3)
            neg_q = bool(exact)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: (a, b, c) is a primitive Pythagorean triple",
    "¬Q: There exists an integer k such that A = k^3"
]

N_HYP = 1
NEG_Q_INDEX = 1