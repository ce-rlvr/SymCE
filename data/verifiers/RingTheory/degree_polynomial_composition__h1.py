import sympy
from sympy import Poly
from sympy.abc import x, y, z

def conditions(witness) -> list[bool]:
    try:
        f, g = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = bool(isinstance(f, Poly) and isinstance(g, Poly) and f.is_univariate and g.is_univariate)
    except Exception:
        h1 = False

    try:
        h2 = bool(f.degree() >= 1 and g.degree() >= 1)
    except Exception:
        h2 = False

    try:
        comp_expr = f.as_expr().subs(f.gen, g.as_expr())
        comp = Poly(comp_expr, f.gen, domain=f.domain)
        neg_q = bool(comp.degree() != f.degree() * g.degree())
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f and g are polynomials",
    "H_2: degrees of f and g are at least 1",
    "¬Q: degree of composition is not the product of degrees"
]

N_HYP = 2
NEG_Q_INDEX = 2