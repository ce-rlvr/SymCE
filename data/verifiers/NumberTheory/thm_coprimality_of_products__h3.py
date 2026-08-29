import math
import sympy

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple or list of three integers: (a, b, c).
    """
    try:
        if len(witness) != 3:
            return [False, False, False]
        a, b, c = witness
    except Exception:
        return [False, False, False]

    # H_1: a, b, and c are integers
    try:
        h1 = isinstance(a, (int, sympy.Integer)) and \
             isinstance(b, (int, sympy.Integer)) and \
             isinstance(c, (int, sympy.Integer))
    except Exception:
        h1 = False

    # H_2: gcd(a, b) = 1
    try:
        h2 = math.gcd(int(a), int(b)) == 1
    except Exception:
        h2 = False

    # ¬Q: gcd(a, b * c) != 1
    try:
        neg_q = math.gcd(int(a), int(b * c)) != 1
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a, b, and c are integers",
    "H_2: gcd(a, b) = 1",
    "¬Q: gcd(a, b * c) != 1"
]

N_HYP = 2
NEG_Q_INDEX = 2