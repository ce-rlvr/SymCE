import math
import sympy

# Top-level setup: no named bindings needed for this number theory conjecture.

def is_int(x):
    if isinstance(x, bool):
        return False
    try:
        return int(x) == x
    except Exception:
        return False

def conditions(witness):
    try:
        a, b, m, d = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = is_int(a) and is_int(b) and is_int(m) and is_int(d) and m > 0
        if h1:
            a, b, m, d = int(a), int(b), int(m), int(d)
    except Exception:
        h1 = False

    try:
        if h1:
            if d == 0:
                h2 = (b == 0)
            else:
                h2 = (b % d == 0)
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        if h1:
            g = math.gcd(a, m)
            if b % g == 0:
                solutions = g
            else:
                solutions = 0
            neg_q = (solutions != d)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a, b, and m are integers with m > 0",
    "H_2: d divides b",
    "¬Q: The linear congruence ax ≡ b (mod m) does NOT have exactly d mutually incongruent solutions modulo m"
]

N_HYP = 2
NEG_Q_INDEX = 2