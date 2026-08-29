import sympy
from sympy import Symbol, Poly

x = Symbol('x')

def conditions(witness) -> list[bool]:
    try:
        poly = Poly(witness)
        if not poly.domain.is_Field:
            poly = poly.set_domain('QQ')
        h1 = (len(poly.gens) <= 1) and poly.domain.is_Field
    except Exception:
        h1 = False

    try:
        poly = Poly(witness)
        h2 = bool(poly.degree() > 0)
    except Exception:
        h2 = False

    try:
        poly = Poly(witness)
        if not poly.domain.is_Field:
            poly = poly.set_domain('QQ')
        _, factors = poly.factor_list()
        neg_q = any(f.degree() > 1 for f, _ in factors)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f(x) is a polynomial over K",
    "H_2: The degree of f(x) is a positive integer n",
    "¬Q: f(x) cannot be factored completely into linear factors over K"
]

N_HYP = 2
NEG_Q_INDEX = 2