import sympy
from sympy.ntheory import isprime, n_order, totient

def conditions(witness):
    """
    Given a witness (p, d), checks if it is a valid counterexample to the false conjecture.
    """
    try:
        p, d = witness
        p = int(p)
        d = int(d)
    except Exception:
        return [False, False]

    # H_1: p is a prime number
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False

    # ¬Q: The number of elements of order d modulo p is NOT exactly phi(d)
    try:
        if d < 1 or p < 2:
            neg_q = False
        else:
            count = 0
            for x in range(1, p):
                try:
                    if n_order(x, p) == d:
                        count += 1
                except Exception:
                    pass
            expected = totient(d)
            neg_q = bool(count != expected)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "¬Q: The number of incongruent integers modulo p with multiplicative order d is not exactly phi(d)"
]

N_HYP = 1
NEG_Q_INDEX = 1