import sympy
from sympy import Rational, sqrt, I, pi, E

def conditions(witness) -> list[bool]:
    try:
        x, y, z = witness
    except Exception:
        return [False, False]
        
    try:
        h1 = bool(sympy.simplify(x**2 + y**2 - 3*z**2) == 0)
    except Exception:
        h1 = False
        
    try:
        x_zero = bool(sympy.simplify(x) == 0)
        y_zero = bool(sympy.simplify(y) == 0)
        z_zero = bool(sympy.simplify(z) == 0)
        neg_q = not (x_zero and y_zero and z_zero)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x^2 + y^2 = 3z^2",
    "¬Q: x, y, and z are not all zero"
]

N_HYP = 1
NEG_Q_INDEX = 1