import sympy

def conditions(witness):
    try:
        a, b, m = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = isinstance(a, (int, sympy.Integer)) and \
             isinstance(b, (int, sympy.Integer)) and \
             isinstance(m, (int, sympy.Integer))
    except Exception:
        h1 = False

    try:
        h2 = m > 0
    except Exception:
        h2 = False

    try:
        neg_q = (b * a) % m != 1 % m
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: a, b, m are integers",
    "H_2: m > 0",
    "¬Q: ba is not congruent to 1 mod m"
]

N_HYP = 2
NEG_Q_INDEX = 2