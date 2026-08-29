import math
from sympy.ntheory import n_order

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks if it is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple (n, a, k) or a dict with these keys.
    """
    try:
        if isinstance(witness, dict):
            n = witness['n']
            a = witness['a']
            k = witness['k']
        else:
            n, a, k = witness
    except Exception:
        return [False, False, False]

    # H_1: n is an integer strictly greater than 1
    try:
        h1 = isinstance(n, int) and not isinstance(n, bool) and n > 1
    except Exception:
        h1 = False

    # H_2: a is an integer coprime to n
    try:
        h2 = isinstance(a, int) and not isinstance(a, bool) and math.gcd(a, n) == 1
    except Exception:
        h2 = False

    # ¬Q: The multiplicative order of the modular inverse of a modulo n is NOT equal to k
    try:
        if h1 and h2:
            inv_a = pow(a, -1, n)
            order_inv = n_order(inv_a, n)
            neg_q = (order_inv != k)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer strictly greater than 1",
    "H_2: a is an integer coprime to n",
    "¬Q: The multiplicative order of the modular inverse of a modulo n is not equal to k"
]

N_HYP = 2
NEG_Q_INDEX = 2