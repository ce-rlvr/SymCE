import sympy
from sympy import Poly
from sympy.abc import x

def conditions(witness) -> list[bool]:
    try:
        f, p = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: f(x) is a polynomial in Z[x] of degree n >= 1
    try:
        poly_f = Poly(f, x, domain='ZZ')
        h1 = bool(poly_f.degree() >= 1)
    except Exception:
        h1 = False

    # H_2: p is a prime number
    try:
        h2 = bool(sympy.isprime(p))
    except Exception:
        h2 = False

    # H_3: p does not divide the leading coefficient of f(x)
    try:
        poly_f = Poly(f, x, domain='ZZ')
        lc = poly_f.LC()
        h3 = bool((lc % p) != 0)
    except Exception:
        h3 = False

    # neg_Q: f(x) is NOT irreducible over Q (i.e., it is reducible over Q)
    try:
        poly_f_qq = Poly(f, x, domain='QQ')
        _, factors = sympy.factor_list(poly_f_qq)
        # Count the total number of non-constant factors (including multiplicity)
        num_factors = sum(mult for factor, mult in factors if factor.degree() >= 1)
        neg_q = bool(num_factors > 1)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: f is a polynomial over Z of degree at least 1",
    "H_2: p is a prime number",
    "H_3: p does not divide the leading coefficient of f",
    "not Q: f is reducible over Q"
]

N_HYP = 3
NEG_Q_INDEX = 3