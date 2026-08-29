import sympy
from sympy import Poly, ZZ, QQ
from sympy.abc import x, y, z

def conditions(witness):
    try:
        h1 = isinstance(witness, Poly) and len(witness.gens) == 1
    except Exception:
        h1 = False

    try:
        h2 = witness.degree() in (2, 3)
    except Exception:
        h2 = False

    try:
        is_irred = witness.is_irreducible
        if is_irred is None:
            neg_q = False
        else:
            roots = witness.ground_roots()
            has_no_roots = (len(roots) == 0)
            neg_q = bool(is_irred != has_no_roots)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f(x) is a polynomial over F",
    "H_2: The degree of f(x) is either 2 or 3",
    "not Q: f(x) is irreducible over F is not equivalent to f(x) having no roots in F"
]

N_HYP = 2
NEG_Q_INDEX = 2