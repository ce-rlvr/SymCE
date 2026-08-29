import sympy
from sympy import Poly
from sympy.abc import x
import math

def is_unit_mod(coeffs, m):
    if not coeffs:
        return False
    c_0 = coeffs[-1]
    if math.gcd(int(c_0), int(m)) != 1:
        return False
    primes = sympy.factorint(m).keys()
    for c in coeffs[:-1]:
        for p in primes:
            if c % p != 0:
                return False
    return True

def is_irreducible_mod(f_poly, m):
    if m < 2:
        return False
    coeffs = f_poly.all_coeffs()
    if is_unit_mod(coeffs, m):
        return False
    factors = sympy.factorint(m)
    if len(factors) == 1:
        p = list(factors.keys())[0]
        try:
            f_mod_p = sympy.Poly(f_poly, domain=sympy.GF(p))
            if f_mod_p.degree() >= 1 and f_mod_p.is_irreducible:
                return True
        except Exception:
            pass
    return False

def conditions(witness):
    try:
        f_expr, m = witness
    except Exception:
        return [False] * 5

    try:
        h1 = True
    except Exception:
        h1 = False

    try:
        f_poly = Poly(f_expr, x, domain='ZZ')
        h2 = f_poly.degree() >= 1
    except Exception:
        h2 = False

    try:
        f_poly = Poly(f_expr, x, domain='ZZ')
        LC = f_poly.LC()
        h3 = (LC % m) != 0
    except Exception:
        h3 = False

    try:
        f_poly = Poly(f_expr, x, domain='ZZ')
        h4 = is_irreducible_mod(f_poly, m)
    except Exception:
        h4 = False

    try:
        factors = sympy.factor_list(f_expr, domain='ZZ')
        num_pos_deg_factors = sum(mult for fac, mult in factors[1] if Poly(fac, x).degree() >= 1)
        neg_q = num_pos_deg_factors >= 2
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: D is a unique factorization domain",
    "H_2: f is a non-constant polynomial over D",
    "H_3: The leading coefficient is not in P",
    "H_4: The image of f modulo P is irreducible",
    "neg_Q: f can be factored into two polynomials of positive degree"
]

N_HYP = 4
NEG_Q_INDEX = 4