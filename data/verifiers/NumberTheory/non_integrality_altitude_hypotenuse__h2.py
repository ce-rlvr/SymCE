import sympy
import math
import itertools
import functools

# Top-level setup
# No specific named bindings needed for this number theory conjecture.

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False, False, False]
        a, b, c = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = (isinstance(a, (int, sympy.Integer)) and 
              isinstance(b, (int, sympy.Integer)) and 
              isinstance(c, (int, sympy.Integer)) and 
              a > 0 and b > 0 and c > 0)
    except Exception:
        h1 = False
        
    try:
        h2 = (a**2 + b**2 == c**2)
    except Exception:
        h2 = False
        
    try:
        neg_q = ((a * b) % c == 0)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a, b, c are positive integers",
    "H_2: a^2 + b^2 = c^2",
    "¬Q: (ab)/c is an integer"
]

N_HYP = 2
NEG_Q_INDEX = 2