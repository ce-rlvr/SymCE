import sympy
from sympy import Poly
from sympy.abc import x

def conditions(witness):
    try:
        expr = sympy.sympify(witness)
        if not expr.free_symbols.issubset({x}):
            h1 = False
        else:
            p = Poly(expr, x)
            h1 = all(c.is_real for c in p.coeffs())
    except Exception:
        h1 = False

    try:
        expr = sympy.sympify(witness)
        p = Poly(expr, x)
        deg = p.degree()
        neg_q = deg not in (1, 2)
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: f(x) is a polynomial over the real numbers",
    "¬Q: The degree of f(x) is not 1 and not 2"
]

N_HYP = 1
NEG_Q_INDEX = 1