import sympy
import math
import itertools
import functools

def conditions(witness) -> list[bool]:
    try:
        x, y, z = witness
        neg_q = (int(x)**4 + int(y)**4 == int(z)**2)
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: x^4 + y^4 == z^2"
]

N_HYP = 0
NEG_Q_INDEX = 0