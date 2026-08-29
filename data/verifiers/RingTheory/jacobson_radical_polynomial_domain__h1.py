import sympy
from sympy.ntheory import factorint

Z2 = 2
Z3 = 3
Z4 = 4
Z6 = 6

def conditions(witness) -> list[bool]:
    try:
        n = int(witness)
        h1 = (n >= 2)
    except Exception:
        h1 = False

    try:
        n = int(witness)
        factors = factorint(n)
        neg_q = any(v > 1 for v in factors.values())
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: polynomial ring over R in one variable",
    "¬Q: Jacobson radical is not the zero ideal"
]

N_HYP = 1
NEG_Q_INDEX = 1