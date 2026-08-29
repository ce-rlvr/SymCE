import sympy
from sympy import abc
import math
import itertools
import functools

# Top-level setup for potential witness expressions
x, y, z = sympy.symbols('x y z')

def _divides(divisor, dividend):
    """Helper to check if divisor divides dividend in Z or Q[x]."""
    if isinstance(divisor, (int, sympy.Integer)) and isinstance(dividend, (int, sympy.Integer)):
        return dividend % divisor == 0
    else:
        q = sympy.cancel(dividend / divisor)
        return q.as_numer_denom()[1] == 1

def conditions(witness):
    try:
        a, b, c = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: a, b, c are non-zero elements in a UFD
    try:
        # We accept integers or sympy expressions (representing elements in Z or Q[x], which are UFDs)
        valid = lambda v: isinstance(v, (int, sympy.Integer, sympy.Expr)) and not isinstance(v, float)
        h1 = bool(a != 0 and b != 0 and c != 0 and valid(a) and valid(b) and valid(c))
    except Exception:
        h1 = False
        
    # H2: a and b are coprime
    try:
        g = sympy.gcd(a, b)
        # In Z and Q[x], the gcd of coprime elements is a unit (1 or -1)
        h2 = bool(g == 1 or g == -1)
    except Exception:
        h2 = False
        
    # H3: a divides c
    try:
        h3 = bool(_divides(a, c))
    except Exception:
        h3 = False
        
    # neg_Q: ab does NOT divide c
    try:
        ab = a * b
        neg_q = not bool(_divides(ab, c))
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: a, b, c are non-zero elements in a UFD",
    "H_2: a and b are coprime",
    "H_3: a divides c",
    "¬Q: ab does not divide c"
]

N_HYP = 3
NEG_Q_INDEX = 3