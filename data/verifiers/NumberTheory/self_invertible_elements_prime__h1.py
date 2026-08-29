import sympy
import math

# Top-level setup
# (No named bindings needed for this number theory conjecture; use integers directly)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            x = witness['x']
            p = witness['p']
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            x, p = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        h1 = isinstance(x, (int, sympy.Integer)) and isinstance(p, (int, sympy.Integer))
    except Exception:
        h1 = False

    try:
        h2 = False
        if h1 and p != 0:
            h2 = (int(x)**2) % int(p) == 1 % int(p)
    except Exception:
        h2 = False

    try:
        neg_q = False
        if h1 and p != 0:
            neg_q = (int(x) % int(p) != 1 % int(p)) and (int(x) % int(p) != (-1) % int(p))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: x and p are integers",
    "H_2: x^2 == 1 (mod p)",
    "¬Q: x != 1 (mod p) and x != -1 (mod p)"
]

N_HYP = 2
NEG_Q_INDEX = 2