import sympy
from sympy import Poly, Symbol
from sympy.ntheory import isprime

x = Symbol('x')

def conditions(witness):
    try:
        poly = Poly(witness, x, domain='ZZ')
        h1 = bool(poly.LC() == 1 and poly.degree() >= 1)
    except Exception:
        h1 = False

    try:
        poly = Poly(witness, x, domain='ZZ')
        a0 = poly.nth(0)
        h2 = bool(isprime(abs(int(a0))))
    except Exception:
        h2 = False

    try:
        poly = Poly(witness, x, domain='ZZ')
        a0 = poly.nth(0)
        p = abs(int(a0))
        coeffs = poly.all_coeffs()
        sum_abs = sum(abs(int(c)) for c in coeffs[1:-1])
        h3 = bool(p > sum_abs)
    except Exception:
        h3 = False

    try:
        poly = Poly(witness, x, domain='QQ')
        neg_q = not poly.is_irreducible
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: f is a monic polynomial in Z",
    "H_2: a_0 is p or -p for some prime p",
    "H_3: p is greater than the sum of absolute values of other coefficients",
    "neg_Q: f is reducible over Q"
]

N_HYP = 3
NEG_Q_INDEX = 3