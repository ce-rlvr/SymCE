import sympy

def conditions(witness):
    try:
        w = sympy.sympify(witness)
        h1 = bool(w.is_integer and w > 0)
    except Exception:
        h1 = False

    try:
        w = sympy.sympify(witness)
        val = sympy.sqrt(w)
        neg_q = (val.is_rational is True)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: sqrt(n) is a rational number"
]

N_HYP = 1
NEG_Q_INDEX = 1