import sympy
from sympy import Poly, isprime, factor_list, Integer
from sympy.abc import x

def conditions(witness):
    try:
        p, f = witness
    except Exception:
        return [False, False, False, False, False, False]

    try:
        poly_f = Poly(f, x)
        h1 = isinstance(p, (int, Integer)) and poly_f.domain.is_ZZ
    except Exception:
        h1 = False

    try:
        h2 = isprime(p)
    except Exception:
        h2 = False

    try:
        h3 = poly_f.degree() >= 1
    except Exception:
        h3 = False

    try:
        a_n = poly_f.LC()
        h4 = (a_n % p) != 0
    except Exception:
        h4 = False

    try:
        a_0 = poly_f.nth(0)
        h5 = (a_0 % (p**2)) != 0
    except Exception:
        h5 = False

    try:
        factors = factor_list(f, domain='ZZ')[1]
        deg_sum = sum(mult for fac, mult in factors if Poly(fac, x).degree() >= 1)
        neg_q = deg_sum >= 2
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: P is a prime ideal of R",
    "H_3: f is a polynomial of degree at least 1",
    "H_4: a_n is not in P",
    "H_5: a_0 is not in P squared",
    "¬Q: f can be factored into two polynomials of positive degree"
]

N_HYP = 5
NEG_Q_INDEX = 5