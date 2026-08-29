import sympy
from sympy.ntheory import divisor_count

def conditions(witness) -> list[bool]:
    try:
        h1 = isinstance(witness, (int, sympy.Integer)) and int(witness) > 0
    except Exception:
        h1 = False

    try:
        if h1:
            neg_q = (divisor_count(int(witness)) % 2 == 0)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: tau(n) is even"
]

N_HYP = 1
NEG_Q_INDEX = 1