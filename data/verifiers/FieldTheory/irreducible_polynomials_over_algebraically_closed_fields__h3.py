import sympy
from sympy import Poly, Symbol

x = Symbol('x')

def conditions(witness):
    h1_ok = False
    h2_ok = False
    neg_q_ok = False
    
    try:
        expr = sympy.sympify(witness)
        h1_ok = True
    except Exception:
        pass

    try:
        expr = sympy.sympify(witness)
        p = Poly(expr, x)
        if expr.free_symbols.issubset({x}):
            h2_ok = True
    except Exception:
        pass

    try:
        expr = sympy.sympify(witness)
        p = Poly(expr, x)
        if p.degree() != 1:
            neg_q_ok = True
    except Exception:
        pass

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "H_2: p(x) is a polynomial over K",
    "¬Q: The degree of p(x) is not exactly 1"
]

N_HYP = 2
NEG_Q_INDEX = 2