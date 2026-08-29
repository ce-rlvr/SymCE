import sympy

def conditions(witness):
    """
    Given a witness tuple (a, x, y, m), checks the hypotheses and the negated conclusion.
    Returns a list of booleans: [H_1, H_2, H_3, neg_Q]
    """
    try:
        # Witness is expected to be a tuple of 4 elements: (a, x, y, m)
        if len(witness) != 4:
            return [False, False, False, False]
        a, x, y, m = witness
    except Exception:
        return [False, False, False, False]

    # H_1: a, x, and y are integers
    try:
        h1 = isinstance(a, (int, sympy.Integer)) and \
             isinstance(x, (int, sympy.Integer)) and \
             isinstance(y, (int, sympy.Integer))
    except Exception:
        h1 = False

    # H_2: m is a positive integer
    try:
        h2 = isinstance(m, (int, sympy.Integer)) and m > 0
    except Exception:
        h2 = False

    # H_3: ax \equiv 1 \pmod m
    try:
        h3 = (a * x) % m == 1 % m
    except Exception:
        h3 = False

    # ¬Q: y \not\equiv a \pmod m
    try:
        neg_q = (y % m) != (a % m)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: a, x, and y are integers",
    "H_2: m is a positive integer",
    "H_3: ax == 1 (mod m)",
    "¬Q: y != a (mod m)"
]

N_HYP = 3
NEG_Q_INDEX = 3