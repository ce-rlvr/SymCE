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
        else:
            x, y = witness
    except Exception:
        return [False, False]
        
    try:
        h1 = (isinstance(x, (int, sympy.Integer)) or (isinstance(x, float) and x.is_integer())) and \
             (isinstance(y, (int, sympy.Integer)) or (isinstance(y, float) and y.is_integer())) and \
             x > 0 and y > 0
    except Exception:
        h1 = False
        
    try:
        neg_q = not (x == 5 and y == 3)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: x and y are positive integers",
    "¬Q: x != 5 or y != 3"
]

N_HYP = 1
NEG_Q_INDEX = 1