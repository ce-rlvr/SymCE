import sympy
from sympy.ntheory import totient

def conditions(witness):
    try:
        h1 = isinstance(witness, (int, sympy.Integer)) and witness > 0
    except Exception:
        h1 = False

    try:
        neg_q = totient(2 * witness) != totient(witness)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: phi(2n) != phi(n)"
]

N_HYP = 1
NEG_Q_INDEX = 1