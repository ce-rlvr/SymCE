import sympy
from sympy.ntheory import totient

def conditions(witness):
    try:
        h1 = isinstance(witness, (int, sympy.Integer)) and not isinstance(witness, bool)
    except Exception:
        h1 = False

    try:
        neg_q = totient(witness) % 2 != 0
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer",
    "¬Q: phi(n) is not even"
]

N_HYP = 1
NEG_Q_INDEX = 1