import sympy
from sympy.ntheory import divisors
import math

def conditions(witness) -> list[bool]:
    # H_1: n is a perfect number
    try:
        n = int(witness)
        if n != witness:
            h1 = False
        elif n <= 0:
            h1 = False
        else:
            h1 = bool(sum(divisors(n)) == 2 * n)
    except Exception:
        h1 = False

    # neg_Q: n is not of the form k(2k-1) for any positive integer k
    try:
        n = int(witness)
        if n != witness:
            neg_q = False
        else:
            disc = 1 + 8 * n
            if disc < 0:
                neg_q = True
            else:
                s = math.isqrt(disc)
                is_hex = False
                if s * s == disc:
                    if (1 + s) % 4 == 0:
                        k = (1 + s) // 4
                        if k > 0:
                            is_hex = True
                neg_q = not is_hex
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a perfect number",
    "¬Q: n is not of the form k(2k-1) for any positive integer k"
]

N_HYP = 1
NEG_Q_INDEX = 1