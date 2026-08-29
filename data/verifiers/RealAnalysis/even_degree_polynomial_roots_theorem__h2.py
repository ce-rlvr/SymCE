import sympy
from sympy import Poly, real_roots
from sympy.abc import x

# Top-level setup
# (No special groups or matrices needed for this real analysis theorem)

def get_real_roots(witness_expr):
    """
    Safely compute real roots of a polynomial expression.
    Falls back to rational approximation if exact root finding fails due to floats/constants.
    """
    try:
        return real_roots(Poly(witness_expr, x))
    except Exception:
        expr = sympy.nsimplify(witness_expr.evalf(), rational=True)
        return real_roots(Poly(expr, x))

def conditions(witness) -> list[bool]:
    try:
        witness_expr = sympy.sympify(witness)
    except Exception:
        return [False, False, False, False]

    # H1: The function P(x) is a polynomial with real coefficients
    try:
        poly = Poly(witness_expr, x)
        h1 = witness_expr.free_symbols <= {x} and all(c.is_real for c in poly.coeffs())
    except Exception:
        h1 = False

    # H2: The leading coefficient of P(x) is positive
    try:
        poly = Poly(witness_expr, x)
        h2 = bool(poly.LC() > 0)
    except Exception:
        h2 = False

    # H3: There exists a real number x_0 such that P(x_0) < 0
    try:
        poly = Poly(witness_expr, x)
        deg = poly.degree()
        if deg == sympy.oo or deg == -sympy.oo:
            h3 = False
        elif deg % 2 == 1:
            # Odd degree polynomials with real coefficients always span (-oo, oo)
            h3 = True
        elif deg == 0:
            h3 = bool(poly.coeffs()[0] < 0)
        else:
            # For even degree, check if the minimum (at a critical point) is negative
            deriv_expr = witness_expr.diff(x)
            crit_points = get_real_roots(deriv_expr)
            h3 = False
            for cp in crit_points:
                val = witness_expr.subs(x, cp).evalf()
                if val < 0:
                    h3 = True
                    break
    except Exception:
        h3 = False

    # neg_Q: The polynomial P(x) does NOT have at least two distinct real roots
    try:
        rr = get_real_roots(witness_expr)
        # Evaluate to float and round to avoid precision issues with fallback roots
        distinct_roots = set(round(float(r.evalf()), 7) for r in rr)
        neg_q = len(distinct_roots) < 2
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: The function P(x) is a polynomial with real coefficients",
    "H_2: The leading coefficient of P(x) is positive",
    "H_3: There exists a real number x_0 such that P(x_0) < 0",
    "¬Q: The polynomial P(x) does NOT have at least two distinct real roots"
]

N_HYP = 3
NEG_Q_INDEX = 3