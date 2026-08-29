import sympy
from sympy import gcd

# Top-level setup for potential witness expressions
x, y, z = sympy.symbols('x y z')

def conditions(witness) -> list[bool]:
    try:
        a, b = witness
    except Exception:
        return [False, False]
    
    try:
        valid_types = (int, sympy.Integer, sympy.Expr)
        if not (isinstance(a, valid_types) and isinstance(b, valid_types)):
            h1_ok = False
        else:
            h1_ok = (a != 0) and (b != 0)
            # Exclude floats as they don't form a UFD in the exact algebraic sense we want to test
            if isinstance(a, float) or isinstance(b, float):
                h1_ok = False
            if isinstance(a, sympy.Expr) and a.has(sympy.Float):
                h1_ok = False
            if isinstance(b, sympy.Expr) and b.has(sympy.Float):
                h1_ok = False
    except Exception:
        h1_ok = False
        
    try:
        g = gcd(a + b, a * b)
        # In a UFD, the gcd is defined up to multiplication by a unit.
        # For integers and polynomials over fields, sympy normalizes the gcd.
        neg_q_ok = (g != 1) and (g != -1)
    except Exception:
        neg_q_ok = False
        
    return [bool(h1_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: a and b are non-zero elements of a UFD",
    "¬Q: The greatest common divisor of a+b and ab is not 1"
]

N_HYP = 1
NEG_Q_INDEX = 1