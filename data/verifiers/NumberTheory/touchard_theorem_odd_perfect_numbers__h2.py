import sympy
from sympy import Integer

def conditions(witness):
    try:
        if not isinstance(witness, (int, sympy.Integer)):
            h1 = False
        else:
            n = int(witness)
            h1 = (n % 2 == 1)
    except Exception:
        h1 = False

    try:
        if not isinstance(witness, (int, sympy.Integer)):
            neg_q = False
        else:
            n = int(witness)
            neg_q = not (n % 12 == 1 or n % 36 == 9)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is an odd integer",
    "¬Q: n is not congruent to 1 mod 12 and n is not congruent to 9 mod 36"
]

N_HYP = 1
NEG_Q_INDEX = 1