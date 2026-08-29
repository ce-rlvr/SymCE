import sympy
from sympy import Poly, sqrt, Rational, sympify
from sympy.abc import x

CONDITION_LABELS = [
    "H_1: Let F be Q(sqrt(-3))",
    "H_2: Let E be the splitting field of f(x) over F",
    "¬Q: The degree of E over F is not 3, or E is not F(7**(1/3))"
]

N_HYP = 2
NEG_Q_INDEX = 2

def splits_completely(witness, ext):
    try:
        expr = sympify(witness)
        p = Poly(expr, x, extension=ext)
        if p.degree() <= 0:
            return True
        _, factors = p.factor_list()
        return all(fac.degree() <= 1 for fac, mult in factors)
    except Exception:
        return False

def conditions(witness):
    h1 = True
    h2 = False
    try:
        expr = sympify(witness)
        if expr.free_symbols.issubset({x}):
            p = Poly(expr, x, extension=[sqrt(-3)])
            h2 = True
    except Exception:
        h2 = False

    neg_q = False
    if h2:
        try:
            ext_F = [sqrt(-3)]
            ext_K = [sqrt(-3), 7**Rational(1, 3)]
            splits_F = splits_completely(witness, ext_F)
            splits_K = splits_completely(witness, ext_K)
            neg_q = not splits_K or splits_F
        except Exception:
            neg_q = False

    return [h1, h2, neg_q]