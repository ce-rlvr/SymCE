import sympy
from sympy import Poly
from sympy.abc import x

# Top-level setup
# x is defined via sympy.abc.x so that witness expressions can use it.
# The witness is expected to be a tuple (p, f_expr) where p is a prime integer 
# (representing the prime ideal pZ in the integral domain Z) and f_expr is a sympy polynomial in x.

def conditions(witness):
    try:
        p, f_expr = witness
    except Exception:
        return [False] * 6
    
    # H_1: Let R be an integral domain.
    # We restrict to R = Z. We check if p is an integer and f_expr is a polynomial with integer coefficients.
    try:
        if not isinstance(p, (int, sympy.Integer)):
            h1 = False
        else:
            f_poly = Poly(f_expr, x)
            h1 = all(isinstance(c, (int, sympy.Integer)) for c in f_poly.all_coeffs())
    except Exception:
        h1 = False

    # H_2: Let P be a prime ideal of R.
    # In Z, this means p is a prime number.
    try:
        h2 = sympy.isprime(int(p))
    except Exception:
        h2 = False

    # H_3: Let f(x) be a polynomial in R[x] of degree n >= 1.
    try:
        f_poly = Poly(f_expr, x)
        n = f_poly.degree()
        h3 = n >= 1
    except Exception:
        h3 = False

    # H_4: Let a_i be an element of P for all 0 <= i < n.
    try:
        f_poly = Poly(f_expr, x)
        coeffs = f_poly.all_coeffs()
        # coeffs is [a_n, a_{n-1}, ..., a_0]
        a_i_list = coeffs[1:]
        h4 = all(int(c) % int(p) == 0 for c in a_i_list)
    except Exception:
        h4 = False

    # H_5: Let a_0 not be an element of the ideal P^2.
    try:
        f_poly = Poly(f_expr, x)
        coeffs = f_poly.all_coeffs()
        a_0 = coeffs[-1]
        h5 = (int(a_0) % (int(p)**2)) != 0
    except Exception:
        h5 = False

    # ¬Q: The polynomial f(x) CAN be expressed as the product of two polynomials in R[x] of strictly positive degree.
    try:
        f_poly = Poly(f_expr, x)
        c, factors = sympy.factor_list(f_poly)
        num_factors = 0
        for factor, mult in factors:
            if hasattr(factor, 'degree'):
                deg = factor.degree()
            else:
                deg = sympy.degree(factor, x)
            if deg >= 1:
                num_factors += mult
        # If the sum of multiplicities of positive degree irreducible factors is >= 2,
        # it can be partitioned into two polynomials of strictly positive degree.
        neg_q = num_factors >= 2
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: P is a prime ideal of R",
    "H_3: f(x) is a polynomial over R of degree n at least 1",
    "H_4: a_i in P for all i from 0 to n-1",
    "H_5: a_0 not in P^2",
    "¬Q: f(x) can be expressed as the product of two polynomials over R of strictly positive degree"
]

N_HYP = 5
NEG_Q_INDEX = 5