import math
import sympy.ntheory

# Top-level setup
# No named bindings needed for this number theory domain

def conditions(witness) -> list[bool]:
    try:
        c1, c2 = witness
    except Exception:
        return [False, False]

    try:
        c1_int = int(c1)
        if c1_int <= 1:
            h1 = False
        else:
            factors = sympy.ntheory.factorint(c1_int)
            h1 = all(p % 4 == 1 for p in factors)
    except Exception:
        h1 = False

    try:
        c1_int = int(c1)
        c2_int = int(c2)
        neg_q = abs(c1_int - c2_int) == 1
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: c_1 is the hypotenuse of a primitive Pythagorean triple",
    "¬Q: The absolute difference |c_1 - c_2| is equal to 1"
]

N_HYP = 1
NEG_Q_INDEX = 1