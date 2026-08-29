import sympy
from sympy import Poly, factor_list
from sympy.abc import x

def conditions(witness) -> list[bool]:
    try:
        f_expr, p_val = witness
    except Exception:
        return [False, False, False, False, False]
        
    try:
        poly_f = Poly(f_expr, x, domain='ZZ')
        coeffs = poly_f.all_coeffs()
        p = sympy.Integer(p_val)
        h1 = True
    except Exception:
        h1 = False

    try:
        n = poly_f.degree()
        h2 = bool(n >= 1)
    except Exception:
        h2 = False

    try:
        a_n = coeffs[0]
        h3 = bool(sympy.isprime(abs(p)) and (a_n % p != 0))
    except Exception:
        h3 = False

    try:
        h4 = bool(all((c % p == 0) for c in coeffs[1:]))
    except Exception:
        h4 = False

    try:
        factors = factor_list(f_expr, x, domain='QQ')[1]
        non_constant_factors_count = sum(mult for fac, mult in factors if Poly(fac, x).degree() > 0)
        neg_q = bool(non_constant_factors_count > 1)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R is a UFD with field of fractions K",
    "H_2: f is a polynomial over R of degree n >= 1",
    "H_3: There exists a prime element p in R such that p does not divide a_n",
    "H_4: p divides a_i for all 0 <= i < n",
    "¬Q: f is reducible over K"
]

N_HYP = 4
NEG_Q_INDEX = 4