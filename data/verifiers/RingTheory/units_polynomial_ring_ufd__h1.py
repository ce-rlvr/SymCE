import sympy

def conditions(witness) -> list[bool]:
    try:
        h1 = isinstance(witness, (int, sympy.Integer)) and int(witness) >= 2
    except Exception:
        h1 = False

    try:
        if h1:
            factors = sympy.factorint(int(witness))
            neg_q = any(exp > 1 for exp in factors.values())
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = ["H_1: R is a ring", "¬Q: The group of units of the polynomial ring is not equal to the group of units of R"]

N_HYP = 1
NEG_Q_INDEX = 1