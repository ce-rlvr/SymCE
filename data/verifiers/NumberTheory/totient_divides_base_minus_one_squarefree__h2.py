import sympy
from sympy.ntheory import totient, factorint

def conditions(witness):
    # H_1: n is a positive integer
    try:
        n = int(witness)
        if n != witness:
            h1 = False
        else:
            h1 = (n > 0)
    except Exception:
        h1 = False

    # H_2: \phi(n) divides n - 1
    try:
        n = int(witness)
        if n != witness:
            h2 = False
        else:
            phi_n = totient(n)
            h2 = ((n - 1) % phi_n == 0)
    except Exception:
        h2 = False

    # ¬Q: n is not a square-free integer
    try:
        n = int(witness)
        if n != witness:
            neg_q = False
        else:
            factors = factorint(n)
            is_sq_free = all(exp == 1 for p, exp in factors.items() if p != -1)
            neg_q = not is_sq_free
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: phi(n) divides n - 1",
    "¬Q: n is not a square-free integer"
]

N_HYP = 2
NEG_Q_INDEX = 2