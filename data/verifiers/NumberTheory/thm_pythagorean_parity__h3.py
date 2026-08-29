import sympy
import math
import itertools
import functools

def conditions(witness):
    try:
        # Witness should be a tuple or list of three elements: (x, y, z)
        if len(witness) != 3:
            return [False, False, False]
        x, y, z = witness
    except Exception:
        return [False, False, False]
    
    # H_1: x, y, z are integers
    try:
        h1 = isinstance(x, (int, sympy.Integer)) and \
             isinstance(y, (int, sympy.Integer)) and \
             isinstance(z, (int, sympy.Integer))
    except Exception:
        h1 = False

    # H_2: x \equiv 1 \pmod 2
    try:
        h2 = (x % 2 == 1)
    except Exception:
        h2 = False

    # ¬Q: x^2 + y^2 == z^2 (Conclusion x^2 + y^2 != z^2 fails)
    try:
        neg_q = (x**2 + y**2 == z**2)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: x, y, z are integers",
    "H_2: x is odd",
    "¬Q: x^2 + y^2 = z^2"
]

N_HYP = 2
NEG_Q_INDEX = 2