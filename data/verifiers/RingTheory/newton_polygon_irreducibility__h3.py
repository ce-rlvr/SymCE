import sympy
import math
from sympy.abc import x

# Top-level setup
# x is imported from sympy.abc to be used in witness expressions

def vp(c, p):
    if c == 0:
        return float('inf')
    c = sympy.Rational(c)
    num = c.p
    den = c.q
    return sympy.multiplicity(p, num) - sympy.multiplicity(p, den)

def conditions(witness):
    try:
        f, p = witness
    except Exception:
        return [False] * 5

    try:
        poly = sympy.Poly(f, x, domain='QQ')
        n = poly.degree()
        h1 = (n >= 1)
    except Exception:
        h1 = False

    try:
        a0 = poly.coeff_monomial(1)
        h2 = (a0 != 0)
    except Exception:
        h2 = False

    try:
        p_int = int(p)
        if p_int < 2 or p_int != p:
            h3 = False
        else:
            an = poly.coeff_monomial(x**n)
            a0_val = poly.coeff_monomial(1)
            if a0_val == 0 or an == 0:
                h3 = False
            else:
                v0 = vp(a0_val, p_int)
                vn = vp(an, p_int)
                h3 = True
                for i in range(1, n):
                    ai = poly.coeff_monomial(x**i)
                    vi = vp(ai, p_int)
                    if n * vi < n * v0 + i * (vn - v0):
                        h3 = False
                        break
    except Exception:
        h3 = False

    try:
        p_int = int(p)
        if p_int < 2 or p_int != p:
            h4 = False
        else:
            an = poly.coeff_monomial(x**n)
            a0_val = poly.coeff_monomial(1)
            if a0_val == 0 or an == 0:
                h4 = False
            else:
                v0 = vp(a0_val, p_int)
                vn = vp(an, p_int)
                h4 = (math.gcd(n, vn - v0) == 1)
    except Exception:
        h4 = False

    try:
        _, factors = sympy.factor_list(f, domain='QQ')
        total_mult = sum(mult for factor, mult in factors if sympy.Poly(factor, x).degree() > 0)
        neg_q = (total_mult > 1)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: f(x) is a polynomial over Q of degree n >= 1",
    "H_2: a_0 != 0",
    "H_3: The p-adic Newton polygon of f(x) consists of a single line segment",
    "H_4: gcd(n, v_p(a_n) - v_p(a_0)) = 1",
    "not Q: f(x) is reducible over Q"
]

N_HYP = 4
NEG_Q_INDEX = 4