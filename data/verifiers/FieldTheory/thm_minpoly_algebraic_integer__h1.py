import sympy
from sympy import minpoly, Poly, Rational, sqrt, I, pi, E, Integer, Float
from sympy.abc import x

def conditions(witness) -> list[bool]:
    try:
        poly = minpoly(witness, x)
        p = Poly(poly, x)
        coeffs = p.coeffs()
        all_ints = all(sympy.sympify(c).is_integer for c in coeffs)
        neg_q = not all_ints
    except Exception:
        neg_q = False
        
    return [bool(neg_q)]

CONDITION_LABELS: list[str] = [
    "¬Q: The minimal polynomial of alpha over Q does not have integer coefficients"
]

N_HYP: int = 0
NEG_Q_INDEX: int = 0