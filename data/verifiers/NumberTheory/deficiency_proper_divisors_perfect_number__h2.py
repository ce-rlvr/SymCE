import sympy
from sympy.ntheory import divisor_sigma

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            n = int(witness['n'])
            d = int(witness['d'])
        elif hasattr(witness, 'n') and hasattr(witness, 'd'):
            n = int(witness.n)
            d = int(witness.d)
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            n = int(witness[0])
            d = int(witness[1])
        else:
            n = int(witness)
            d = int(witness)
    except Exception:
        return [False, False]

    # H_1: n is a perfect number
    try:
        h1 = (n > 0) and (divisor_sigma(n) == 2 * n)
    except Exception:
        h1 = False

    # ¬Q: sigma(d) >= 2d
    try:
        neg_q = (d > 0) and (divisor_sigma(d) >= 2 * d)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a perfect number",
    "¬Q: sigma(d) >= 2d"
]

N_HYP = 1
NEG_Q_INDEX = 1