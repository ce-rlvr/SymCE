import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
# Number theory domain primarily uses integers and algebraic numbers directly.

CONDITION_LABELS = [
    "H_1: gcd(a, b) = 1",
    "H_2: m and n are positive integers",
    "¬Q: gcd(a^m, b^n) != 1"
]

N_HYP = 2
NEG_Q_INDEX = 2

def is_pos_int(val):
    """Helper to check if a value is a strictly positive integer."""
    return isinstance(val, (int, sympy.Integer)) and not isinstance(val, bool) and val > 0

def conditions(witness) -> list[bool]:
    try:
        a, b, m, n = witness
    except Exception:
        return [False, False, False]
    
    # H_1: gcd(a, b) = 1
    try:
        h1 = (sympy.gcd(a, b) == 1)
    except Exception:
        h1 = False
        
    # H_2: m and n are positive integers
    try:
        h2 = is_pos_int(m) and is_pos_int(n)
    except Exception:
        h2 = False
        
    # ¬Q: gcd(a^m, b^n) != 1
    try:
        # Expand powers to ensure algebraic numbers (like (1 + sqrt(-5))^2) are simplified
        am = sympy.expand(a**m)
        bn = sympy.expand(b**n)
        neg_q = (sympy.gcd(am, bn) != 1)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]