import math
from sympy import divisors

def conditions(witness) -> list[bool]:
    try:
        witness_tuple = tuple(witness)
        if len(witness_tuple) != 3:
            return [False, False, False]
        a, b, d = witness_tuple
    except Exception:
        return [False, False, False]

    try:
        a_int = int(a)
        b_int = int(b)
        h1 = (a_int == a) and (b_int == b) and (a_int > 0) and (b_int > 0)
        if isinstance(a, bool) or isinstance(b, bool):
            h1 = False
    except Exception:
        h1 = False

    try:
        h2 = False
        if h1:
            h2 = math.gcd(a_int, b_int) == 1
    except Exception:
        h2 = False

    try:
        if not h1:
            neg_q = False
        else:
            divs_a = divisors(a_int)
            divs_b = divisors(b_int)
            count = 0
            for d1 in divs_a:
                for d2 in divs_b:
                    if d1 * d2 == d:
                        count += 1
            neg_q = (count != 1)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    r"H_1: a and b are positive integers",
    r"H_2: \gcd(a, b) = 1",
    r"¬Q: There do not exist unique positive integers d_1 and d_2 such that d_1 divides a, d_2 divides b, and d = d_1 d_2"
]

N_HYP = 2
NEG_Q_INDEX = 2