import sympy
from sympy import Poly

x = sympy.Symbol('x')

def conditions(witness):
    try:
        f, p = witness
    except Exception:
        return [False] * 6
    
    try:
        Poly(f, x, domain='ZZ')
        h1 = isinstance(p, (int, sympy.Integer))
    except Exception:
        h1 = False

    try:
        poly_f = Poly(f, x, domain='ZZ')
        h2 = poly_f.degree() >= 1
    except Exception:
        h2 = False

    try:
        h3 = sympy.isprime(abs(p))
    except Exception:
        h3 = False

    try:
        poly_f = Poly(f, x, domain='ZZ')
        a_n = poly_f.LC()
        h4 = (a_n % p) != 0
    except Exception:
        h4 = False

    try:
        poly_f = Poly(f, x, domain='ZZ')
        a_0 = poly_f.nth(0)
        h5 = (a_0 % (p**2)) != 0
    except Exception:
        h5 = False

    try:
        poly_f_Q = Poly(f, x, domain='QQ')
        factors = poly_f_Q.factor_list()
        mult_sum = sum(exp for fac, exp in factors[1] if fac.degree() >= 1)
        neg_q = mult_sum > 1
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain with fraction field K",
    "H_2: f is a polynomial over R of degree n >= 1",
    "H_3: p is a prime element in R",
    "H_4: p does not divide a_n",
    "H_5: p^2 does not divide a_0",
    "not Q: f is reducible over the fraction field K"
]

N_HYP = 5
NEG_Q_INDEX = 5