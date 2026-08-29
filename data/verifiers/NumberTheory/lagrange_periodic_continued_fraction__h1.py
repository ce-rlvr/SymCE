import sympy
from sympy import minpoly
from sympy.ntheory import continued_fraction_periodic
from sympy.abc import x

def conditions(witness) -> list[bool]:
    # H_1: x is a root of an irreducible quadratic polynomial with integer coefficients
    try:
        w = sympy.sympify(witness)
        poly_expr = minpoly(w, x)
        poly = sympy.Poly(poly_expr, x)
        h1 = bool(poly.degree() == 2 and all(c.is_integer for c in poly.coeffs()))
    except Exception:
        h1 = False

    # ¬Q: The simple continued fraction expansion of x is not eventually periodic
    try:
        w = sympy.sympify(witness)
        if w.is_real:
            # For real numbers, try to compute the periodic continued fraction.
            # If it succeeds, the expansion is eventually periodic.
            res = continued_fraction_periodic(w)
            neg_q = False
        else:
            # Non-real numbers do not have an eventually periodic simple continued fraction.
            neg_q = True
    except Exception:
        # If computation fails (e.g., not a quadratic irrational), it is not eventually periodic.
        neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x is a root of an irreducible quadratic polynomial with integer coefficients",
    "¬Q: The simple continued fraction expansion of x is not eventually periodic"
]

N_HYP = 1
NEG_Q_INDEX = 1