import math

def conditions(witness):
    """
    Given a witness (a, b, c), checks if it satisfies the remaining hypotheses
    and falsifies the conclusion.
    """
    try:
        # Witness is expected to be a tuple or list of three elements
        a, b, c = witness
    except Exception:
        return [False, False, False]

    # H_1: a, b, and c are positive integers
    try:
        h1 = (isinstance(a, int) and isinstance(b, int) and isinstance(c, int) and 
              a > 0 and b > 0 and c > 0)
    except Exception:
        h1 = False

    # H_2: a^2 + b^2 = c^2
    try:
        h2 = (a**2 + b**2 == c**2)
    except Exception:
        h2 = False

    # ¬Q: c^2 is NOT congruent to 1 modulo 24
    try:
        neg_q = (c**2 % 24 != 1)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a, b, and c are positive integers",
    "H_2: a^2 + b^2 = c^2",
    "¬Q: c^2 is not congruent to 1 modulo 24"
]

N_HYP = 2
NEG_Q_INDEX = 2