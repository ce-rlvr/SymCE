import sympy
from sympy.ntheory import mobius
import math

def conditions(witness) -> list[bool]:
    try:
        h1 = isinstance(witness, (int, sympy.Integer)) and not isinstance(witness, bool) and int(witness) > 0
    except Exception:
        h1 = False

    h2 = True

    try:
        if isinstance(witness, (int, sympy.Integer)) and not isinstance(witness, bool):
            n = int(witness)
            if n < 1:
                s = 0
            else:
                s = sum(mobius(k) * (n // k) for k in range(1, n + 1))
            neg_q = (s != 1)
        else:
            n_float = float(witness)
            upper = math.floor(n_float)
            if upper < 1:
                s = 0
            else:
                s = sum(mobius(k) * math.floor(n_float / k) for k in range(1, upper + 1))
            neg_q = (s != 1)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: floor(x) denotes the greatest integer less than or equal to x",
    "¬Q: sum_{k=1}^n mu(k) floor(n/k) != 1"
]

N_HYP = 2
NEG_Q_INDEX = 2