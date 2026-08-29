import sympy
from sympy import Poly, ZZ

x = sympy.Symbol('x')

def conditions(witness):
    try:
        if isinstance(witness, dict):
            f = witness['f']
            g = witness['g']
        else:
            f, g = witness
    except Exception:
        return [False, False, False]

    # H_1: R is a Unique Factorization Domain and f, g are polynomials
    try:
        poly_f = Poly(f, x, domain=ZZ)
        poly_g = Poly(g, x, domain=ZZ)
        h1_ok = True
    except Exception:
        h1_ok = False

    # H_2: f is a primitive polynomial
    try:
        h2_ok = bool(abs(poly_f.content()) == 1)
    except Exception:
        h2_ok = False

    # neg_Q: fg is not a primitive polynomial
    try:
        poly_fg = Poly(f * g, x, domain=ZZ)
        neg_q_ok = bool(abs(poly_fg.content()) != 1)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain and f, g are polynomials",
    "H_2: f is a primitive polynomial",
    "¬Q: fg is not a primitive polynomial"
]

N_HYP = 2
NEG_Q_INDEX = 2