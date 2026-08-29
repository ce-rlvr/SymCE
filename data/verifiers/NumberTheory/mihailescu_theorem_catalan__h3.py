import sympy
from sympy import Integer

def conditions(witness):
    try:
        if isinstance(witness, dict):
            x = witness['x']
            y = witness['y']
            a = witness['a']
            b = witness['b']
        else:
            x, y, a, b = witness
    except Exception:
        return [False, False, False]

    # H1: x, y, a, and b are integers
    try:
        h1 = True
        for v in (x, y, a, b):
            if not isinstance(v, (int, Integer)):
                h1 = False
                break
    except Exception:
        h1 = False

    # H2: x > 1, y > 1, a > 1, and b > 1
    try:
        h2 = all(v > 1 for v in (x, y, a, b))
    except Exception:
        h2 = False

    # neg_Q: The only solution is x=3, a=2, y=2, and b=3.
    try:
        neg_q = not (x == 3 and a == 2 and y == 2 and b == 3)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: x, y, a, and b are integers",
    "H_2: x > 1, y > 1, a > 1, and b > 1",
    "¬Q: The solution is not x=3, a=2, y=2, and b=3"
]

N_HYP = 2
NEG_Q_INDEX = 2