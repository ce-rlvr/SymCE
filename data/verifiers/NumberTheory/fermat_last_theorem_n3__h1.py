import sympy
import math
import itertools
import functools

def conditions(witness) -> list[bool]:
    try:
        x, y, z = witness
        if not (isinstance(x, (int, sympy.Integer)) and 
                isinstance(y, (int, sympy.Integer)) and 
                isinstance(z, (int, sympy.Integer))):
            neg_q = False
        else:
            neg_q = bool(x**3 + y**3 == z**3)
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: x^3 + y^3 == z^3"
]

N_HYP = 0
NEG_Q_INDEX = 0