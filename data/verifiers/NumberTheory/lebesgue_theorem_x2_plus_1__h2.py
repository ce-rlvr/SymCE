import sympy
from sympy import Integer

# Top-level setup
# (No named bindings needed for this number theory conjecture)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 3:
            return [False, False]
        x, y, n = witness
    except Exception:
        return [False, False]

    try:
        h1 = (isinstance(x, (int, Integer)) and 
              isinstance(y, (int, Integer)) and 
              isinstance(n, (int, Integer)) and 
              x > 0 and y > 0 and n > 0)
    except Exception:
        h1 = False

    try:
        if isinstance(n, (int, Integer)) and n > 100000:
            neg_q = False
        else:
            neg_q = (x**2 + 1 == y**n)
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: x, y, n are positive integers",
    "¬Q: x^2 + 1 = y^n"
]

N_HYP = 1
NEG_Q_INDEX = 1