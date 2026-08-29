import sympy
from sympy import Integer
from sympy.ntheory import divisor_sigma

def conditions(witness):
    try:
        h1 = isinstance(witness, (int, Integer)) and witness > 0
    except Exception:
        h1 = False

    try:
        neg_q = divisor_sigma(witness) % 2 == 0
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: sigma(n) is an even integer"
]

N_HYP = 1
NEG_Q_INDEX = 1