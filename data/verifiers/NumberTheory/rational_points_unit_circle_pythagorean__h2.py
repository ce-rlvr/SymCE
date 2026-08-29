import sympy
from sympy import Rational

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            h1 = False
        else:
            x, y = witness
            x_rat = Rational(x)
            y_rat = Rational(y)
            h1 = bool(x_rat > 0 and y_rat > 0)
    except Exception:
        h1 = False

    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            neg_q = False
        else:
            x, y = witness
            x_rat = Rational(x)
            y_rat = Rational(y)
            neg_q = bool((x_rat <= 0) or (y_rat <= 0) or (x_rat**2 + y_rat**2 != 1))
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x and y are positive rational numbers",
    "¬Q: There do not exist positive integers a, b, c such that a^2 + b^2 = c^2, x = a/c, and y = b/c"
]

N_HYP = 1
NEG_Q_INDEX = 1