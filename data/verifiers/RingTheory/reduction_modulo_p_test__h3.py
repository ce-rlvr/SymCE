import sympy
from sympy import Poly, isprime
from sympy.abc import x

def conditions(witness) -> list[bool]:
    try:
        f, p = witness
        poly_f = Poly(f, x)
        h1 = (poly_f.domain == sympy.ZZ) and (poly_f.degree() >= 1)
    except Exception:
        h1 = False

    try:
        f, p = witness
        h2 = bool(isprime(p))
    except Exception:
        h2 = False

    try:
        f, p = witness
        poly_f = Poly(f, x, domain='ZZ')
        poly_mod = poly_f.trunc(p)
        if poly_mod.is_zero or poly_mod.degree() < 1:
            h3 = False
        else:
            factors = sympy.factor_list(poly_mod.as_expr(), x, modulus=p)
            h3 = (len(factors[1]) == 1 and factors[1][0][1] == 1)
    except Exception:
        h3 = False

    try:
        f, p = witness
        factors = sympy.factor_list(f, x, domain='QQ')
        num_factors = sum(mult for fac, mult in factors[1])
        neg_q = num_factors > 1
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: f is a polynomial with integer coefficients of degree at least 1",
    "H_2: p is a prime number",
    "H_3: The reduction of f modulo p is irreducible over Z_p",
    "¬Q: f is reducible over Q"
]

N_HYP = 3
NEG_Q_INDEX = 3