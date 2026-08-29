import sympy as sp
from sympy.abc import x, y, z
from sympy import Rational, Integer

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain with field of fractions K",
    "H_2: f(x) is a polynomial over R of degree n >= 1",
    "H_3: p divides a_i for all 0 <= i < n",
    "H_4: p^2 does not divide a_0",
    "neg_Q: f(x) is reducible over K"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness):
    try:
        f, p = witness
    except Exception:
        return [False] * 5

    # H1: R is a UFD (we use Z, so check if p is a prime element in Z)
    try:
        p_val = int(p)
        h1 = sp.isprime(abs(p_val))
    except Exception:
        h1 = False

    # H2: f(x) is a polynomial in R[x] of degree n >= 1
    try:
        free_syms = f.free_symbols if hasattr(f, 'free_symbols') else set()
        if len(free_syms) == 1:
            var = list(free_syms)[0]
        elif len(free_syms) == 0:
            var = sp.Symbol('x')
        else:
            var = None
        
        if var is not None:
            f_poly = sp.Poly(f, var)
            is_ZZ_poly = True
            for c in f_poly.all_coeffs():
                try:
                    if not sp.Rational(c).is_Integer:
                        is_ZZ_poly = False
                        break
                except Exception:
                    is_ZZ_poly = False
                    break
            h2 = is_ZZ_poly and f_poly.degree() >= 1
        else:
            h2 = False
    except Exception:
        h2 = False

    # H3: p | a_i for 0 <= i < n
    try:
        if h2:
            coeffs = f_poly.all_coeffs()
            # a_i for 0 <= i < n are all coefficients except the leading one
            a_i_list = coeffs[1:]
            h3 = all(int(sp.Rational(c)) % p_val == 0 for c in a_i_list)
        else:
            h3 = False
    except Exception:
        h3 = False

    # H4: p^2 \nmid a_0
    try:
        if h2:
            a_0 = coeffs[-1]
            h4 = (int(sp.Rational(a_0)) % (p_val**2)) != 0
        else:
            h4 = False
    except Exception:
        h4 = False

    # neg_Q: f(x) is reducible over K (QQ)
    try:
        if h2:
            factors = sp.factor_list(f_poly, domain='QQ')[1]
            num_factors = sum(mult for fac, mult in factors if fac.degree() >= 1)
            neg_q = num_factors > 1
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]