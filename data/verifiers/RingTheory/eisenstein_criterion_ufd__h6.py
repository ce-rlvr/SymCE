import sympy
from sympy import Poly
from sympy.abc import x

def conditions(witness) -> list[bool]:
    try:
        f_expr, p = witness
    except Exception:
        return [False] * 6
        
    try:
        f_poly = Poly(f_expr, domain='ZZ')
        if len(f_poly.gens) == 0:
            f_poly = Poly(f_expr, x, domain='ZZ')
        elif len(f_poly.gens) > 1:
            f_poly = None
    except Exception:
        f_poly = None

    try:
        if f_poly is not None and (isinstance(p, int) or p.is_integer):
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    try:
        h2 = f_poly.degree() >= 1
    except Exception:
        h2 = False

    try:
        h3 = sympy.isprime(abs(int(p)))
    except Exception:
        h3 = False

    try:
        coeffs = f_poly.all_coeffs()
        a_i = coeffs[1:]
        h4 = all(int(c) % int(p) == 0 for c in a_i)
    except Exception:
        h4 = False

    try:
        a_n = coeffs[0]
        h5 = int(a_n) % int(p) != 0
    except Exception:
        h5 = False

    try:
        factors = sympy.factor_list(f_poly, domain='QQ')
        num_factors = sum(exp for poly, exp in factors[1] if poly.degree() > 0)
        neg_q = num_factors > 1
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = ["H_1: R is a UFD", "H_2: f(x) is a polynomial of degree n >= 1", "H_3: p is a prime element in R", "H_4: p divides a_i for all 0 <= i < n", "H_5: p does not divide a_n", "not Q: f(x) is reducible over K"]

N_HYP = 5
NEG_Q_INDEX = 5