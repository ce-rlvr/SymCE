import sympy
from sympy import totient

def conditions(witness):
    """
    Checks whether the given witness satisfies the remaining hypotheses
    and falsifies the conclusion of the conjecture.
    """
    try:
        n = int(witness)
        h1 = bool(n > 6)
    except Exception:
        h1 = False

    try:
        n = int(witness)
        if n < 1:
            neg_q = False
        else:
            # The conclusion is phi(n) >= sqrt(n).
            # Its negation is phi(n) < sqrt(n), which is equivalent to phi(n)^2 < n
            # since phi(n) is always positive for n >= 1.
            neg_q = bool(totient(n)**2 < n)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n > 6",
    "¬Q: phi(n) < sqrt(n)"
]

N_HYP = 1
NEG_Q_INDEX = 1