import sympy
import math
import itertools
import functools

# Top-level setup
# No specific named bindings needed for this number theory conjecture.

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            x = witness['x']
            y = witness['y']
            z = witness['z']
        else:
            x, y, z = witness
            
        h1 = (isinstance(x, (int, sympy.Integer)) and 
              isinstance(y, (int, sympy.Integer)) and 
              isinstance(z, (int, sympy.Integer)))
    except Exception:
        h1 = False

    try:
        if isinstance(witness, dict):
            x = witness['x']
            y = witness['y']
            z = witness['z']
        else:
            x, y, z = witness
            
        neg_q = not (x == 0 and y == 0 and z == 0)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x, y, z are integers",
    "¬Q: x, y, z are not all zero"
]

N_HYP = 1
NEG_Q_INDEX = 1