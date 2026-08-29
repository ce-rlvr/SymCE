import sympy
from sympy import Poly, isprime
from sympy.abc import x

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            p = witness['p']
            g = witness['g']
            m = witness['m']
            n = witness['n']
            f = witness.get('f', g**n + p*m)
        elif len(witness) == 5:
            f, g, m, n, p = witness
        elif len(witness) == 4:
            g, m, n, p = witness
            f = g**n + p*m
        else:
            return [False] * 6
    except Exception:
        return [False] * 6

    # H1: p is a prime number
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False

    # H2: g(x) in Z[x] is monic
    try:
        g_poly = Poly(g, x)
        h2 = bool(g_poly.is_monic and all(c.is_integer for c in g_poly.coeffs()))
    except Exception:
        h2 = False

    # H3: reduction of g(x) mod p is irreducible in (Z/pZ)[x]
    try:
        g_mod_p = Poly(g, x, domain=sympy.GF(p))
        h3 = bool(g_mod_p.is_irreducible)
    except Exception:
        h3 = False

    # H4: degree of m(x) is strictly less than n * deg(g)
    try:
        m_poly = Poly(m, x)
        h4 = bool(m_poly.degree() < n * g_poly.degree())
    except Exception:
        h4 = False

    # H5: reduction of m(x) mod p is not divisible by reduction of g(x) mod p
    try:
        m_mod_p = Poly(m, x, domain=sympy.GF(p))
        rem = m_mod_p % g_mod_p
        h5 = bool(not rem.is_zero)
    except Exception:
        h5 = False

    # neg_Q: f(x) is reducible in Q[x]
    try:
        f_poly = Poly(f, x, domain='QQ')
        neg_q = bool(not f_poly.is_irreducible)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: g(x) is monic",
    "H_3: reduction of g(x) modulo p is irreducible",
    "H_4: degree of m(x) is strictly less than n * deg(g)",
    "H_5: reduction of m(x) modulo p is not divisible by reduction of g(x)",
    "¬Q: f(x) is reducible over Q"
]

N_HYP = 5
NEG_Q_INDEX = 5