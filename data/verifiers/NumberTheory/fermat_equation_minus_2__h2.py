import sympy

def conditions(witness):
    try:
        if len(witness) != 2:
            h1 = False
        else:
            x, y = witness
            x_sym = sympy.sympify(x)
            y_sym = sympy.sympify(y)
            h1 = x_sym.is_integer and y_sym.is_integer
    except Exception:
        h1 = False

    try:
        if len(witness) != 2:
            neg_q = False
        else:
            x, y = witness
            neg_q = not (x == 3 and (y == -5 or y == 5))
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: x, y in Z",
    "¬Q: not (x = 3 and y in {-5, 5})"
]

N_HYP = 1
NEG_Q_INDEX = 1