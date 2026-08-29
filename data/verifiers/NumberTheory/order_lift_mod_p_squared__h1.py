import math
from sympy.ntheory import n_order

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            p = witness.get('p')
            k = witness.get('k', None)
        else:
            if len(witness) == 2:
                a, p = witness
                k = None
            elif len(witness) == 3:
                a, p, k = witness
            else:
                return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: a is an integer coprime to p
    try:
        h1 = isinstance(a, int) and isinstance(p, int) and p > 1 and math.gcd(a, p) == 1
    except Exception:
        h1 = False

    # H_2: The order of a modulo p is k
    try:
        if not h1:
            h2 = False
        else:
            actual_k = n_order(a, p)
            if k is None:
                k = actual_k
                h2 = True
            else:
                h2 = isinstance(k, int) and (actual_k == k)
    except Exception:
        h2 = False

    # ¬Q: The order of a modulo p^2 is neither k nor p k
    try:
        if not h1 or not isinstance(k, int):
            neg_q = False
        else:
            ord_p2 = n_order(a, p**2)
            neg_q = (ord_p2 != k) and (ord_p2 != p * k)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a is an integer coprime to p",
    "H_2: The order of a modulo p is k",
    "¬Q: The order of a modulo p^2 is neither k nor p k"
]

N_HYP = 2
NEG_Q_INDEX = 2