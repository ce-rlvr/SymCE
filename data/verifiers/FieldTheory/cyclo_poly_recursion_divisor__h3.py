import sympy
from sympy.polys import cyclotomic_poly
from sympy.abc import x
from sympy.ntheory import isprime

def conditions(witness):
    try:
        n, p = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = (isinstance(n, int) or isinstance(n, sympy.Integer)) and n >= 1
    except Exception:
        h1 = False

    try:
        h2 = (isinstance(p, int) or isinstance(p, sympy.Integer)) and isprime(p)
    except Exception:
        h2 = False

    try:
        if h1 and h2:
            poly_pn = cyclotomic_poly(p * n, x)
            poly_n_xp = cyclotomic_poly(n, x**p)
            diff = sympy.expand(poly_pn - poly_n_xp)
            neg_q = bool(diff != 0)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n >= 1 is an integer",
    "H_2: p is a prime number",
    "¬Q: Phi_{pn}(x) != Phi_n(x^p)"
]

N_HYP = 2
NEG_Q_INDEX = 2