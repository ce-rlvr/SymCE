import math

def conditions(witness):
    """
    Given a witness (a, b, c), checks the remaining hypotheses and the negated conclusion.
    """
    try:
        a, b, c = witness
        a = int(a)
        b = int(b)
        c = int(c)
    except Exception:
        return [False, False, False, False]
    
    # H_1: gcd(a, b, c) = 1
    try:
        h1 = (math.gcd(math.gcd(a, b), c) == 1)
    except Exception:
        h1 = False

    # H_2: a is an even integer
    try:
        h2 = (a % 2 == 0)
    except Exception:
        h2 = False

    # H_3: b is an odd integer
    try:
        h3 = (b % 2 == 1)
    except Exception:
        h3 = False

    # ¬Q: gcd(c - a, c - b) != 1
    try:
        neg_q = (math.gcd(c - a, c - b) != 1)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: gcd(a, b, c) = 1",
    "H_2: a is an even integer",
    "H_3: b is an odd integer",
    "¬Q: gcd(c - a, c - b) != 1"
]

N_HYP = 3
NEG_Q_INDEX = 3