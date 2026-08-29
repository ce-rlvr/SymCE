import sympy

# No specific named object bindings needed for this number theory conjecture.

def conditions(witness) -> list[bool]:
    try:
        # Witness is expected to be a tuple: (m, a, b, c)
        if len(witness) != 4:
            return [False, False, False, False]
        m, a, b, c = witness
    except Exception:
        return [False, False, False, False]

    # H_1: m is a positive integer
    try:
        h1 = isinstance(m, (int, sympy.Integer)) and m > 0
    except Exception:
        h1 = False

    # H_2: a, b, c are integers
    try:
        h2 = isinstance(a, (int, sympy.Integer)) and \
             isinstance(b, (int, sympy.Integer)) and \
             isinstance(c, (int, sympy.Integer))
    except Exception:
        h2 = False

    # H_3: ac ≡ 1 (mod m)
    try:
        h3 = (a * c - 1) % m == 0
    except Exception:
        h3 = False

    # ¬Q: b ≢ c (mod m)
    try:
        neg_q = (b - c) % m != 0
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: m is a positive integer",
    "H_2: a, b, c are integers",
    "H_3: ac ≡ 1 (mod m)",
    "¬Q: b ≢ c (mod m)"
]

N_HYP = 3
NEG_Q_INDEX = 3