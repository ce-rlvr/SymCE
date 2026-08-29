import math

def conditions(witness):
    try:
        n, a, b = witness
    except Exception:
        return [False, False, False, False]

    # H1: n is an integer strictly greater than 1
    try:
        h1 = isinstance(n, int) and not isinstance(n, bool) and n > 1
    except Exception:
        h1 = False

    # H2: a and b are integers
    try:
        h2 = isinstance(a, int) and not isinstance(a, bool) and isinstance(b, int) and not isinstance(b, bool)
    except Exception:
        h2 = False

    # H3: a is invertible modulo n
    try:
        h3 = h1 and h2 and math.gcd(a, n) == 1
    except Exception:
        h3 = False

    # neg_Q: The product ab is invertible modulo n, and its modular inverse is congruent to a^{-1}b^{-1} (mod n).
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            def eval_conclusion():
                try:
                    inv_ab = pow(a * b, -1, n)
                    inv_a = pow(a, -1, n)
                    inv_b = pow(b, -1, n)
                    return inv_ab == (inv_a * inv_b) % n
                except Exception:
                    return False
            neg_q = not eval_conclusion()
    except Exception:
        neg_q = True

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer strictly greater than 1",
    "H_2: a and b are integers",
    "H_3: a is invertible modulo n",
    "¬Q: ab is not invertible modulo n, or its inverse is not congruent to a^{-1}b^{-1} (mod n)"
]

N_HYP = 3
NEG_Q_INDEX = 3