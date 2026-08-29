import sympy
import math
import itertools
import functools

# Top-level setup
# (No named bindings needed for this number theory conjecture)

def conditions(witness) -> list[bool]:
    try:
        x, y, z = witness
        x = int(x)
        y = int(y)
        z = int(z)
        neg_q = (x**4 + 2 * y**4 == z**2)
    except Exception:
        neg_q = False
    
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: x^4 + 2y^4 == z^2"
]

N_HYP = 0
NEG_Q_INDEX = 0