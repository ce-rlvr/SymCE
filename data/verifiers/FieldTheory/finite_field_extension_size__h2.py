import sympy
from sympy.abc import x

def conditions(witness):
    try:
        if len(witness) != 2:
            return [False, False, False]
        q, poly_expr = witness
    except Exception:
        return [False, False, False]

    try:
        q_int = int(q)
        factors = sympy.factorint(q_int)
        h1 = (len(factors) == 1) and (q_int > 1)
    except Exception:
        h1 = False

    try:
        q_int = int(q)
        poly_gf = sympy.Poly(poly_expr, x, domain=sympy.GF(q_int))
        n = poly_gf.degree()
        h2 = bool(n >= 1)
    except Exception:
        h2 = False

    try:
        if not (h1 and h2):
            neg_q = False
        else:
            q_int = int(q)
            poly_gf = sympy.Poly(poly_expr, x, domain=sympy.GF(q_int))
            is_field = poly_gf.is_irreducible
            neg_q = not is_field
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a finite field containing exactly q elements",
    "H_2: The degree of the extension K:F is a finite integer n",
    "¬Q: K is not a finite field containing exactly q^n elements"
]

N_HYP = 2
NEG_Q_INDEX = 2