import sympy
from sympy import Poly
from sympy.abc import x
import math

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        f, c = witness
    except Exception:
        return [False, False, False]

    # H1: f(x) in Z[x] of degree n >= 1
    try:
        f_poly = Poly(f, x)
        h1 = bool(f_poly.domain == sympy.ZZ and f_poly.degree() >= 1)
    except Exception:
        h1 = False

    # H2: c > 1 + max{|alpha| : f(alpha) = 0}
    try:
        f_poly = Poly(f, x)
        exact_roots = sympy.roots(f_poly, multiple=True)
        if len(exact_roots) == f_poly.degree():
            roots = exact_roots
        else:
            roots = f_poly.nroots()
            
        if roots:
            max_root_abs = max(abs(complex(r)) for r in roots)
        else:
            max_root_abs = 0.0
        h2 = bool(float(c) > 1.0 + max_root_abs)
    except Exception:
        h2 = False

    # neg_Q: f(x) is reducible over Q
    try:
        f_poly = Poly(f, x)
        factors = sympy.factor_list(f_poly, domain='QQ')
        num_factors = sum(exp for p, exp in factors[1] if p.degree() >= 1)
        neg_q = bool(num_factors > 1)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a polynomial in Z over x of degree at least 1",
    "H_2: c is greater than 1 plus the max absolute value of roots of f",
    "not Q: f is reducible over Q"
]

N_HYP = 2
NEG_Q_INDEX = 2