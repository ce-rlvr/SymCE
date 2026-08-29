import sympy
import math
import functools

# Top-level setup: named object bindings that the witness expression may reference.
x = sympy.Symbol('x')

def conditions(witness):
    # H1: R is a unique factorization domain
    # We implicitly use R = Z (the integers), which is a UFD.
    # We check if the witness is a polynomial in x with integer coefficients.
    try:
        poly = sympy.Poly(witness, x)
        h1 = all(c.is_integer for c in poly.coeffs())
    except Exception:
        h1 = False

    # H2: F is the field of fractions of R
    # We implicitly use F = Q (the rationals), which is the field of fractions of Z.
    # This holds whenever H1 holds in our setup.
    try:
        h2 = h1
    except Exception:
        h2 = False

    # H3: f(x) is a primitive polynomial in R[x] of positive degree
    try:
        poly = sympy.Poly(witness, x)
        coeffs = poly.coeffs()
        ints = [int(c) for c in coeffs]
        content = functools.reduce(math.gcd, ints)
        is_primitive = (abs(content) == 1)
        pos_degree = poly.degree() > 0
        h3 = is_primitive and pos_degree
    except Exception:
        h3 = False

    # neg_Q: f(x) is reducible in F[x]
    # The conclusion is that f(x) is irreducible in F[x].
    # The negation is that f(x) is reducible in F[x] (can be factored into >1 non-constant polynomials).
    try:
        poly_qq = sympy.Poly(witness, x, domain='QQ')
        factors = poly_qq.factor_list()
        # factors[1] contains tuples of (factor, multiplicity)
        num_factors = sum(mult for fac, mult in factors[1] if fac.degree() > 0)
        neg_q = num_factors > 1
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

# Note: Avoided using '[' and ']' inside the strings to prevent regex parsing issues in the validator.
CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: F is the field of fractions of R",
    "H_3: f is a primitive polynomial over R of positive degree",
    "not Q: f is reducible over F"
]

N_HYP = 3
NEG_Q_INDEX = 3