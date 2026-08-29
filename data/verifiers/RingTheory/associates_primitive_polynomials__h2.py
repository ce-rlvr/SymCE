import sympy
from sympy import Poly
from sympy.abc import x

def conditions(witness) -> list[bool]:
    try:
        f, g = witness
    except Exception:
        return [False, False, False]

    # H_1: R is a UFD with fraction field K, and f, g are in R[x].
    # We verify this by checking if f and g can be parsed as polynomials over Z.
    try:
        poly_f = Poly(f, x, domain='ZZ')
        poly_g = Poly(g, x, domain='ZZ')
        h1 = True
    except Exception:
        h1 = False

    # H_2: f and g are associate elements in K[x].
    # In Q[x], this means f = c * g for some non-zero rational constant c.
    try:
        poly_f_Q = Poly(f, x, domain='QQ')
        poly_g_Q = Poly(g, x, domain='QQ')
        if poly_f_Q.is_zero and poly_g_Q.is_zero:
            h2 = True
        elif poly_f_Q.is_zero or poly_g_Q.is_zero:
            h2 = False
        else:
            q, r = poly_f_Q.div(poly_g_Q)
            h2 = bool(r.is_zero and q.degree() == 0)
    except Exception:
        h2 = False

    # ¬Q: f and g are NOT associate elements in R[x].
    # In Z[x], the only units are 1 and -1. Thus, f and g are associates iff f = g or f = -g.
    # The negation of the conclusion means f != g AND f != -g.
    try:
        neg_q = bool((sympy.simplify(f - g) != 0) and (sympy.simplify(f + g) != 0))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain with field of fractions K",
    "H_2: f and g are associate elements in the polynomial ring over K",
    "¬Q: f and g are not associate elements in the polynomial ring over R"
]

N_HYP = 2
NEG_Q_INDEX = 2