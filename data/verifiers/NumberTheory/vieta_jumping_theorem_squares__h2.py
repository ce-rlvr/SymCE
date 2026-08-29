import math

def conditions(witness) -> list[bool]:
    try:
        if not (isinstance(witness, (tuple, list)) and len(witness) == 2):
            h1 = False
        else:
            a, b = witness
            if isinstance(a, bool) or isinstance(b, bool):
                h1 = False
            elif int(a) != a or int(b) != b:
                h1 = False
            else:
                a = int(a)
                b = int(b)
                h1 = (a > 0 and b > 0)
    except Exception:
        h1 = False

    try:
        a, b = witness
        a = int(a)
        b = int(b)
        num = a**2 + b**2
        den = a*b + 1
        if den == 0:
            q = False
        elif num % den == 0:
            k = num // den
            if k < 0:
                q = False
            else:
                root = math.isqrt(k)
                q = (root * root == k)
        else:
            q = False
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a and b are positive integers",
    "¬Q: The integer quotient (a^2 + b^2) / (ab + 1) is not a perfect square"
]

N_HYP = 1
NEG_Q_INDEX = 1