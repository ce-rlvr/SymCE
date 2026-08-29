import sympy
import functools
from sympy import Poly
from sympy.abc import x, y, z

N_HYP = 4
NEG_Q_INDEX = 4

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: F is the field of fractions of R",
    "H_3: f and g are polynomials over R",
    "H_4: f is a primitive polynomial",
    "neg_Q: f does not divide g in the polynomial ring"
]

def is_poly_over_ZZ(expr):
    expr = sympy.sympify(expr)
    if expr.is_Integer:
        return True
    if expr.is_Rational and not expr.is_Integer:
        return False
    try:
        syms = list(expr.free_symbols)
        if not syms:
            return expr.is_Integer
        p = sympy.Poly(expr, *syms)
        return p.domain.is_ZZ
    except Exception:
        return False

def conditions(witness):
    try:
        f, g = witness
    except Exception:
        return [False] * 5

    # H1: R is a UFD
    # We enforce R to be a polynomial ring over ZZ in the variables other than x.
    # Such a ring is always a UFD.
    try:
        f = sympy.sympify(f)
        g = sympy.sympify(g)
        h1 = True
    except Exception:
        h1 = False

    # H2: F is the field of fractions of R
    # This is a definitional statement for the context of the theorem.
    h2 = h1

    # H3: f and g are polynomials over R
    # This means they are polynomials in x, and their coefficients are in R (polynomials over ZZ).
    try:
        poly_f = sympy.Poly(f, x)
        poly_g = sympy.Poly(g, x)
        
        h3 = True
        for c in poly_f.coeffs() + poly_g.coeffs():
            if not is_poly_over_ZZ(c):
                h3 = False
                break
    except Exception:
        h3 = False

    # H4: f is primitive
    # The content of f is the gcd of its coefficients. It must be a unit in R.
    # Since R is ZZ[...], the only units are 1 and -1.
    try:
        coeffs = poly_f.coeffs()
        if not coeffs:
            h4 = False
        else:
            content = functools.reduce(sympy.gcd, coeffs)
            content = sympy.sympify(content)
            h4 = (content == 1 or content == -1)
    except Exception:
        h4 = False

    # neg_Q: f does not divide g in the polynomial ring
    try:
        domain = poly_f.domain.unify(poly_g.domain)
        pf = poly_f.set_domain(domain)
        pg = poly_g.set_domain(domain)
        q, r = pg.div(pf)
        divides = r.is_zero
        neg_q = not divides
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]