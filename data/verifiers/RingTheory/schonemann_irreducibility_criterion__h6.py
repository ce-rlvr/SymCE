import sympy
from sympy import Poly, isprime, degree, LC
from sympy.abc import x
from sympy.polys.polytools import factor_list

CONDITION_LABELS = [
    "H_1: f = g^n + p*m over Z",
    "H_2: p is prime",
    "H_3: g is monic",
    "H_4: g mod p is irreducible",
    "H_5: deg(m) < n*deg(g)",
    "¬Q: f is reducible over Q"
]

N_HYP = 5
NEG_Q_INDEX = 5

def conditions(witness):
    try:
        f, g, m, p, n = witness
    except Exception:
        return [False] * 6

    try:
        f_poly = Poly(f, x, domain='ZZ')
        g_poly = Poly(g, x, domain='ZZ')
        m_poly = Poly(m, x, domain='ZZ')
        h1 = bool(f_poly == g_poly**n + p * m_poly) and (n == int(n)) and (n >= 1)
    except Exception:
        h1 = False

    try:
        h2 = bool(isprime(p))
    except Exception:
        h2 = False

    try:
        h3 = bool(LC(g, x) == 1)
    except Exception:
        h3 = False

    try:
        factors = factor_list(g, x, modulus=p)
        h4 = (len(factors[1]) == 1 and factors[1][0][1] == 1 and degree(factors[1][0][0], x) == degree(g, x))
        h4 = bool(h4 and degree(g, x) >= 1)
    except Exception:
        h4 = False

    try:
        if Poly(m, x).is_zero:
            deg_m = -1
        else:
            deg_m = degree(m, x)
        h5 = bool(deg_m < n * degree(g, x))
    except Exception:
        h5 = False

    try:
        factors_f = factor_list(f, x, domain='QQ')
        num_factors = sum(mult for fac, mult in factors_f[1] if degree(fac, x) >= 1)
        neg_q = bool(num_factors != 1)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]