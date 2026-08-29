import sympy
from sympy.ntheory import factorint

def conditions(witness):
    try:
        p, n = witness
    except Exception:
        return [False, False]

    # H_1: n is a positive integer
    try:
        h1 = (int(n) == n) and (int(n) > 0)
    except Exception:
        h1 = False

    # ¬Q: p^n is not a prime power (so no finite field of order p^n exists)
    try:
        if int(p) != p:
            neg_q = False
        else:
            q = int(p) ** int(n)
            if q <= 1:
                neg_q = True
            else:
                factors = factorint(q)
                neg_q = len(factors) != 1
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: p^n is not a prime power (no finite field of order p^n exists)"
]

N_HYP = 1
NEG_Q_INDEX = 1