import sympy

def conditions(witness) -> list[bool]:
    # H_1: x, y \in \mathbb{Z}
    try:
        if len(witness) != 2:
            h1 = False
        else:
            x, y = witness
            h1 = isinstance(x, (int, sympy.Integer)) and isinstance(y, (int, sympy.Integer))
    except Exception:
        h1 = False

    # ¬Q: not (x == 0 and y == 0)
    try:
        if len(witness) != 2:
            neg_q = False
        else:
            x, y = witness
            neg_q = not (x == 0 and y == 0)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x, y in Z",
    "¬Q: x != 0 or y != 0"
]

N_HYP = 1
NEG_Q_INDEX = 1