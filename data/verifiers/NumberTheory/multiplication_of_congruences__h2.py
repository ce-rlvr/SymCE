import sympy
from sympy import Integer

def conditions(witness) -> list[bool]:
    try:
        a, b, c, d, m = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = (isinstance(a, (int, Integer)) and
              isinstance(b, (int, Integer)) and
              isinstance(c, (int, Integer)) and
              isinstance(d, (int, Integer)) and
              isinstance(m, (int, Integer)) and
              m > 0)
    except Exception:
        h1 = False

    try:
        h2 = (c - d) % m == 0
    except Exception:
        h2 = False

    try:
        neg_q = (a * c - b * d) % m != 0
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: a, b, c, d, m are integers with m > 0",
    "H_2: c \\equiv d \\pmod m",
    "¬Q: ac \\not\\equiv bd \\pmod m"
]

N_HYP = 2
NEG_Q_INDEX = 2