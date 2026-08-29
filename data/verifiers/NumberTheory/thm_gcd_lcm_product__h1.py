import sympy
import math
import itertools
import functools
from sympy import gcd, lcm

# Top-level setup
# No specific named bindings required for Number Theory

def conditions(witness):
    try:
        a, b = witness
    except Exception:
        return [False, False]
        
    try:
        h1 = bool(a > 0 and b > 0)
    except Exception:
        h1 = False
        
    try:
        g = gcd(a, b)
        l = lcm(a, b)
        left = g * l
        right = a * b
        
        if hasattr(left, 'equals'):
            eq = left.equals(right)
            if eq is True:
                neg_q = False
            elif eq is False:
                neg_q = True
            else:
                neg_q = bool(sympy.simplify(left - right) != 0)
        else:
            neg_q = bool(left != right)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: a > 0 and b > 0",
    "¬Q: gcd(a, b) * lcm(a, b) != a * b"
]

N_HYP = 1
NEG_Q_INDEX = 1