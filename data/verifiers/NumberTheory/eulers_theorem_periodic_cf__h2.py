import sympy
from sympy import sympify, minpoly, degree, pi, E, I, sqrt, Rational, Integer
from sympy.polys.polyerrors import NotAlgebraic

# Top-level setup
# (No specific named groups or matrices needed for this number theory conjecture)

CONDITION_LABELS = [
    "H_1: x is a real number",
    "¬Q: x is not a quadratic irrational"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    try:
        x = sympify(witness)
    except Exception:
        return [False, False]

    # H_1: x is a real number
    try:
        h1 = x.is_real
        if h1 is None:
            h1 = x.evalf().is_real
        h1 = bool(h1)
    except Exception:
        h1 = False

    # ¬Q: x is not a quadratic irrational
    try:
        poly = minpoly(x)
        deg = degree(poly)
        neg_q = bool(deg != 2)
    except NotAlgebraic:
        neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]