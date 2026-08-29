import math
import sympy
from sympy import totient
from sympy.ntheory import n_order

# Top-level setup
# (No specific named bindings required for this number theory conjecture)

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks the hypotheses and the negated conclusion.
    The witness is expected to be a dictionary {'n': n, 'a': a, 'k': k}
    or a tuple (n, a, k).
    """
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            a = witness.get('a')
            k = witness.get('k')
        elif isinstance(witness, (tuple, list)) and len(witness) == 3:
            n, a, k = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: n is a positive integer
    try:
        h1 = False
        if not isinstance(n, bool):
            if int(n) == n and n > 0:
                h1 = True
                n = int(n)
    except Exception:
        h1 = False

    # H_2: a is an integer
    try:
        h2 = False
        if not isinstance(a, bool):
            if int(a) == a:
                h2 = True
                a = int(a)
    except Exception:
        h2 = False

    # H_3: k is the multiplicative order of a modulo n
    try:
        h3 = False
        if h1 and h2 and not isinstance(k, bool):
            if int(k) == k and k > 0:
                k_int = int(k)
                if math.gcd(a, n) == 1:
                    h3 = bool(k_int == n_order(a, n))
                elif n == 1:
                    h3 = bool(k_int == 1)
    except Exception:
        h3 = False

    # ¬Q: k does not divide \phi(n)
    try:
        neg_q = False
        if h1 and not isinstance(k, bool):
            if int(k) == k and k != 0:
                k_int = int(k)
                phi_n = totient(n)
                neg_q = bool(phi_n % k_int != 0)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: a is an integer",
    "H_3: k is the multiplicative order of a modulo n",
    "¬Q: k does not divide phi(n)"
]

N_HYP = 3
NEG_Q_INDEX = 3