import math

def conditions(witness):
    try:
        p = int(witness)
        if p != witness:
            return [False, False]
    except Exception:
        return [False, False]

    try:
        h1 = bool(p >= 5)
    except Exception:
        h1 = False

    try:
        if p < 3:
            neg_q = False
        elif p > 100000:
            neg_q = False
        else:
            fact = math.factorial(p - 3)
            q = (fact * (p - 2)) % p == 1
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p >= 5",
    "¬Q: The modular inverse of (p-3)! modulo p is not congruent to p-2 (mod p)"
]

N_HYP = 1
NEG_Q_INDEX = 1