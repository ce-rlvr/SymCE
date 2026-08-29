import math

def conditions(witness):
    """
    Given a witness (a, b, c), checks if it satisfies the remaining hypotheses
    and falsifies the conclusion.
    """
    try:
        if len(witness) != 3:
            return [False, False, False]
        a, b, c = witness
    except Exception:
        return [False, False, False]

    # H_1: a, b, and c are positive integers
    try:
        h1 = (int(a) == a) and (int(b) == b) and (int(c) == c) and (a > 0) and (b > 0) and (c > 0)
    except Exception:
        h1 = False

    # H_2: gcd(a, b, c) = 1
    try:
        h2 = math.gcd(math.gcd(int(a), int(b)), int(c)) == 1
    except Exception:
        h2 = False

    # ¬Q: The sum a + b is NOT congruent to either 1 or 7 modulo 8
    try:
        neg_q = ((int(a) + int(b)) % 8) not in (1, 7)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a, b, and c are positive integers",
    "H_2: gcd(a, b, c) = 1",
    "¬Q: a + b is not congruent to 1 or 7 modulo 8"
]

N_HYP = 2
NEG_Q_INDEX = 2