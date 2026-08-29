import sympy
from sympy import Poly, factor_list
from sympy.abc import x

N_HYP = 5
NEG_Q_INDEX = 5

CONDITION_LABELS = [
    "H_1: R is a UFD with fraction field K",
    "H_2: f is a polynomial over R of degree n >= 1",
    "H_3: p is a prime element in R",
    "H_4: p divides a_i for all 0 <= i < n",
    "H_5: p^2 does not divide a_0",
    "not Q: f is reducible over the fraction field K"
]

def conditions(witness):
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False] * 6
        f_expr, p = witness
    except Exception:
        return [False] * 6

    try:
        f_poly = Poly(f_expr, x)
        h1 = bool(f_poly.domain.is_ZZ and sympy.S(p).is_integer)
    except Exception:
        h1 = False

    try:
        n = f_poly.degree()
        h2 = bool(n >= 1)
    except Exception:
        h2 = False

    try:
        h3 = bool(sympy.isprime(abs(int(p))))
    except Exception:
        h3 = False

    try:
        coeffs = f_poly.all_coeffs()
        a_i_list = coeffs[1:]
        h4 = all(sympy.S(c % p).is_zero for c in a_i_list)
    except Exception:
        h4 = False

    try:
        a_0 = coeffs[-1]
        h5 = not sympy.S(a_0 % (p**2)).is_zero
    except Exception:
        h5 = False

    try:
        factors = factor_list(f_expr, x, domain='QQ')
        num_factors = sum(mult for fac, mult in factors[1] if Poly(fac, x).degree() >= 1)
        neg_q = bool(num_factors > 1)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]