import sympy
from sympy import Poly, isprime, GF
from sympy.abc import x

def conditions(witness):
    try:
        if isinstance(witness, dict):
            f = witness.get('f')
            g = witness.get('g')
            m = witness.get('m')
            n = witness.get('n')
            p = witness.get('p')
        else:
            f, g, m, n, p = witness
    except Exception:
        return [False] * 6

    try:
        f_poly = Poly(f, x, domain='ZZ')
        g_poly = Poly(g, x, domain='ZZ')
        m_poly = Poly(m, x, domain='ZZ')
        n_val = int(n)
        p_val = int(p)
        h1 = bool(n_val >= 1 and f_poly == g_poly**n_val + p_val * m_poly)
    except Exception:
        h1 = False

    try:
        h2 = bool(isprime(p_val))
    except Exception:
        h2 = False

    try:
        h3 = bool(g_poly.LC() == 1)
    except Exception:
        h3 = False

    try:
        h4 = bool(m_poly.degree() < n_val * g_poly.degree())
    except Exception:
        h4 = False

    try:
        m_mod_p = Poly(m_poly, domain=GF(p_val))
        g_mod_p = Poly(g_poly, domain=GF(p_val))
        _, rem = m_mod_p.div(g_mod_p)
        h5 = bool(not rem.is_zero)
    except Exception:
        h5 = False

    try:
        f_Q = Poly(f_poly, domain='QQ')
        factors = f_Q.factor_list()
        num_factors = sum(mult for fac, mult in factors[1] if fac.degree() > 0)
        neg_q = bool(num_factors > 1)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: f(x) = g(x)^n + p m(x) is a polynomial with integer coefficients",
    "H_2: p is a prime number",
    "H_3: g(x) is monic",
    "H_4: deg(m) < n deg(g)",
    "H_5: m(x) mod p is not divisible by g(x) mod p",
    "not Q: f(x) is reducible over the rationals"
]

N_HYP = 5
NEG_Q_INDEX = 5