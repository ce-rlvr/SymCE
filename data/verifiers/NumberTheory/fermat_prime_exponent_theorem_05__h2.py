import sympy
import math

# Top-level setup
# (No named bindings needed for this number theory conjecture)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, (int, sympy.Integer)):
            h1 = bool(witness > 0)
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        if isinstance(witness, (int, sympy.Integer)):
            n = int(witness)
            is_power_of_2 = (n > 0) and ((n & (n - 1)) == 0)
            neg_q = not is_power_of_2
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: n is not a power of 2"
]

N_HYP = 1
NEG_Q_INDEX = 1