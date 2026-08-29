import sympy
import math
import itertools
import functools

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the conjecture:
    Hypotheses:
      - m is a positive integer
      - a == b (mod m)
      - c == d (mod m)
    Conclusion:
      - a - c == b - d (mod m)
    """
    try:
        if isinstance(witness, dict):
            m = witness['m']
            a = witness['a']
            b = witness['b']
            c = witness['c']
            d = witness['d']
        else:
            m, a, b, c, d = witness
    except Exception:
        return [False, False, False, False]

    # H_1: m is a positive integer
    try:
        h1 = (int(m) == m) and (m > 0)
    except Exception:
        h1 = False

    # H_2: a == b (mod m)
    try:
        h2 = (a - b) % m == 0
    except Exception:
        h2 = False

    # H_3: c == d (mod m)
    try:
        h3 = (c - d) % m == 0
    except Exception:
        h3 = False

    # ¬Q: a - c != b - d (mod m)
    try:
        neg_q = ((a - c) - (b - d)) % m != 0
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: m is a positive integer",
    "H_2: a == b (mod m)",
    "H_3: c == d (mod m)",
    "¬Q: a - c != b - d (mod m)"
]

N_HYP = 3
NEG_Q_INDEX = 3