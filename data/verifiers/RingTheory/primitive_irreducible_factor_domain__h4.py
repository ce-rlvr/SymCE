import sympy
from sympy import Symbol, Poly, ZZ, QQ
from sympy.abc import x

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain (UFD)",
    "H_2: f(x) is a non-constant polynomial over R",
    "H_3: The content of f(x) is 1",
    "¬Q: The factor ring over R modulo f(x) is not an integral domain"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        R, f = witness
    except Exception:
        return [False, False, False, False]

    try:
        h1 = bool(R.is_UFD)
    except Exception:
        h1 = False

    try:
        if not isinstance(f, sympy.Poly):
            f_poly = sympy.Poly(f, x, domain=R)
        else:
            f_poly = f
        h2 = bool(f_poly.degree() > 0 and f_poly.domain == R and len(f_poly.gens) == 1)
    except Exception:
        h2 = False

    try:
        if not isinstance(f, sympy.Poly):
            f_poly = sympy.Poly(f, x, domain=R)
        else:
            f_poly = f
        cont = f_poly.content()
        if hasattr(R, 'is_unit'):
            h3 = bool(R.is_unit(cont))
        else:
            h3 = bool(cont == R.one or cont == -R.one)
    except Exception:
        h3 = False

    try:
        if not isinstance(f, sympy.Poly):
            f_poly = sympy.Poly(f, x, domain=R)
        else:
            f_poly = f
        neg_q = (f_poly.is_irreducible == False)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]