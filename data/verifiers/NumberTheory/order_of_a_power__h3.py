import math
from sympy.ntheory import n_order

def conditions(witness):
    """
    Given a witness (n, a, h, k) or a dictionary with these keys,
    checks the remaining hypotheses and the negated conclusion.
    """
    try:
        if isinstance(witness, dict):
            n = witness['n']
            a = witness['a']
            h = witness['h']
            k = witness['k']
        elif isinstance(witness, (tuple, list)) and len(witness) == 4:
            n, a, h, k = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: n is an integer greater than 1
    try:
        h1 = isinstance(n, int) and n > 1
    except Exception:
        h1 = False

    # H_2: a is an integer coprime to n
    try:
        h2 = isinstance(a, int) and isinstance(n, int) and math.gcd(a, n) == 1
    except Exception:
        h2 = False

    # H_3: h is a positive integer
    try:
        h3 = isinstance(h, int) and h > 0
    except Exception:
        h3 = False

    # ¬Q: The multiplicative order of a^h modulo n is not equal to k / gcd(h, k)
    try:
        if not (isinstance(k, int) and isinstance(h, int) and isinstance(n, int) and isinstance(a, int)):
            neg_q = False
        else:
            val = pow(a, h, n)
            actual_order = n_order(val, n)
            g = math.gcd(h, k)
            if g == 0:
                neg_q = True
            else:
                expected_order = k / g
                neg_q = actual_order != expected_order
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer greater than 1",
    "H_2: a is an integer coprime to n",
    "H_3: h is a positive integer",
    "¬Q: The multiplicative order of a^h modulo n is not equal to k / gcd(h, k)"
]

N_HYP = 3
NEG_Q_INDEX = 3