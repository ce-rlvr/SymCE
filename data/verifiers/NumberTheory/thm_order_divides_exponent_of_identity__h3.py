import math
from sympy.ntheory import n_order

def conditions(witness):
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            a = witness.get('a')
            k = witness.get('k')
        else:
            n, a, k = witness
    except Exception:
        n, a, k = None, None, None

    try:
        h1 = isinstance(n, int) and not isinstance(n, bool) and n > 1
    except Exception:
        h1 = False

    try:
        h2 = (isinstance(a, int) and not isinstance(a, bool) and 
              isinstance(n, int) and not isinstance(n, bool) and 
              math.gcd(a, n) == 1)
    except Exception:
        h2 = False

    try:
        if (isinstance(n, int) and not isinstance(n, bool) and 
            isinstance(a, int) and not isinstance(a, bool) and 
            isinstance(k, int) and not isinstance(k, bool)):
            order = n_order(a, n)
            neg_q = (k % order != 0)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer greater than 1",
    "H_2: a is an integer coprime to n",
    "¬Q: The multiplicative order of a modulo n does not divide k"
]

N_HYP = 2
NEG_Q_INDEX = 2