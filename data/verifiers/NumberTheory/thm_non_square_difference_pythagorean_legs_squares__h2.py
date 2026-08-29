import math

def conditions(witness):
    try:
        w = list(witness)
        if len(w) != 3:
            return [False, False]
        a, b, c = w
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
        diff = abs(a_int**2 - b_int**2)
        root = math.isqrt(diff)
        neg_q = (root**2 == diff)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: (a, b, c) is a Pythagorean triple consisting of positive integers",
    "¬Q: |a^2 - b^2| is equal to k^2 for some integer k"
]

N_HYP = 1
NEG_Q_INDEX = 1