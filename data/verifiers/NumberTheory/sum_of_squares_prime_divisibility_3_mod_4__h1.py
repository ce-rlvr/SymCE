import sympy

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False, False, False]
        p, a, b = witness
    except Exception:
        return [False, False, False, False]

    try:
        h1 = isinstance(p, (int, sympy.Integer)) and (int(p) % 4 == 3)
    except Exception:
        h1 = False

    try:
        h2 = isinstance(a, (int, sympy.Integer)) and isinstance(b, (int, sympy.Integer))
    except Exception:
        h2 = False

    try:
        h3 = (int(a)**2 + int(b)**2) % int(p) == 0
    except Exception:
        h3 = False

    try:
        neg_q = (int(a) % int(p) != 0) or (int(b) % int(p) != 0)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: p = 3 mod 4",
    "H_2: a and b are integers",
    "H_3: p divides a^2 + b^2",
    "¬Q: p does not divide a or p does not divide b"
]

N_HYP = 3
NEG_Q_INDEX = 3