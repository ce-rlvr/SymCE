import sympy
from sympy.ntheory import divisor_sigma

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            d = witness['d']
            n = witness['n']
        else:
            d, n = witness
    except Exception:
        return [False, False]

    try:
        h1 = isinstance(n, (int, sympy.Integer)) and n > 0
    except Exception:
        h1 = False

    try:
        if isinstance(d, (int, sympy.Integer)) and d > 0 and isinstance(n, (int, sympy.Integer)) and n > 0:
            neg_q = bool(divisor_sigma(d) >= divisor_sigma(n))
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: sigma(d) >= sigma(n)"
]

N_HYP = 1
NEG_Q_INDEX = 1