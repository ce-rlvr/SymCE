import sympy
from sympy import Poly
from sympy.abc import x, y
import math

def conditions(witness):
    try:
        f, g = witness
        f = sympy.sympify(f)
        g = sympy.sympify(g)
    except Exception:
        return [False] * 6

    # H_1: K is a field
    try:
        poly_f = Poly(f, x, y)
        poly_g = Poly(g, x, y)
        h1 = True
    except Exception:
        h1 = False

    # H_2: g(y) \in K[y]
    try:
        h2 = x not in g.free_symbols
    except Exception:
        h2 = False

    # H_3: deg(f) >= 1
    try:
        deg_f = int(Poly(f, x, y).total_degree())
        h3 = deg_f >= 1
    except Exception:
        h3 = False

    # H_4: deg(g) >= 1
    try:
        deg_g = int(Poly(g, y).degree())
        h4 = deg_g >= 1
    except Exception:
        h4 = False

    # H_5: gcd(deg(f), deg(g)) == 1
    try:
        h5 = math.gcd(deg_f, deg_g) == 1
    except Exception:
        h5 = False

    # neg_Q: f(x) - g(y) is NOT irreducible in K[x,y]
    try:
        fg = f - g
        poly_fg = Poly(fg, x, y)
        field_domain = poly_fg.domain.get_field()
        poly_fg_field = Poly(fg, x, y, domain=field_domain)
        
        factors = poly_fg_field.factor_list()
        num_factors = sum(mult for fac, mult in factors[1] if fac.total_degree() > 0)
        
        neg_q = num_factors != 1
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(h5), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: g is a polynomial in y",
    "H_3: deg f >= 1",
    "H_4: deg g >= 1",
    "H_5: gcd of degrees is 1",
    "not Q: f - g is not irreducible"
]

N_HYP = 5
NEG_Q_INDEX = 5