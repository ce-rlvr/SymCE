import sympy

def conditions(witness) -> list[bool]:
    try:
        x, y = witness
        h1 = isinstance(x, (int, sympy.Integer)) and isinstance(y, (int, sympy.Integer))
    except Exception:
        h1 = False

    try:
        x, y = witness
        neg_q = (int(x), int(y)) not in {(1, 1), (1, -1), (-1, 1), (-1, -1)}
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x and y are integers",
    "¬Q: (x,y) is not in {(1,1), (1,-1), (-1,1), (-1,-1)}"
]

N_HYP = 1
NEG_Q_INDEX = 1