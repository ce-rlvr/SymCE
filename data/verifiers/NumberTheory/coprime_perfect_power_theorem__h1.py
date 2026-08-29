import math
from sympy import integer_nthroot

# Top-level setup
# No named bindings needed for this number theory problem.

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 4:
            return [False, False, False]
        a, b, c, n = witness
        if int(a) != a or int(b) != b or int(c) != c or int(n) != n:
            return [False, False, False]
        a, b, c, n = int(a), int(b), int(c), int(n)
    except Exception:
        return [False, False, False]

    # H_1: gcd(a, b) == 1
    try:
        h1_ok = (math.gcd(a, b) == 1)
    except Exception:
        h1_ok = False

    # H_2: a * b == c**n
    try:
        if c in (0, 1, -1):
            if c == 0 and n < 0:
                h2_ok = False
            else:
                h2_ok = (a * b == c**n)
        elif n > 10**5 or n < -10**5:
            h2_ok = False
        else:
            h2_ok = (a * b == c**n)
    except Exception:
        h2_ok = False

    # neg_Q: not (exists u > 0, v > 0: a == u**n and b == v**n)
    try:
        def is_nth_power_of_positive_integer(val, p):
            if val <= 0:
                return False
            if p == 0:
                return val == 1
            if p < 0:
                return val == 1
            root, exact = integer_nthroot(val, p)
            return bool(exact and root > 0)
        
        q = is_nth_power_of_positive_integer(a, n) and is_nth_power_of_positive_integer(b, n)
        neg_q_ok = not q
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: gcd(a, b) = 1",
    "H_2: a b = c^n",
    "¬Q: a and b are not both n-th powers of positive integers"
]

N_HYP = 2
NEG_Q_INDEX = 2