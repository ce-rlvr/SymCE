import sympy
from sympy import Symbol, Poly, isprime, expand
from sympy.polys.domains import ZZ, QQ, GF

# Top-level setup
x = Symbol('x')

def conditions(witness) -> list[bool]:
    try:
        f, g, m, n, p = witness
    except Exception:
        return [False] * 6

    # H1: f(x) = g(x)^n + p m(x) in Z[x]
    try:
        f_poly = Poly(f, x, domain=ZZ)
        g_poly = Poly(g, x, domain=ZZ)
        m_poly = Poly(m, x, domain=ZZ)
        n_int = int(n)
        p_int = int(p)
        
        expr_eq = expand(f_poly.as_expr() - (g_poly.as_expr()**n_int + p_int * m_poly.as_expr())) == 0
        h1 = (n_int >= 1) and expr_eq
    except Exception:
        h1 = False

    # H2: p is a prime number
    try:
        h2 = bool(isprime(p_int))
    except Exception:
        h2 = False

    # H3: g(x) is monic
    try:
        h3 = (g_poly.LC() == 1)
    except Exception:
        h3 = False

    # H4: g(x) mod p is irreducible in (Z/pZ)[x]
    try:
        g_mod_p = Poly(g, x, domain=GF(p_int))
        h4 = bool(g_mod_p.is_irreducible)
    except Exception:
        h4 = False

    # H5: m(x) mod p is not divisible by g(x) mod p
    try:
        m_mod_p = Poly(m, x, domain=GF(p_int))
        g_mod_p = Poly(g, x, domain=GF(p_int))
        r = m_mod_p % g_mod_p
        h5 = not bool(r.is_zero)
    except Exception:
        h5 = False

    # neg_Q: f(x) is reducible in Q[x]
    try:
        f_Q = Poly(f, x, domain=QQ)
        neg_q = not bool(f_Q.is_irreducible)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: f(x) = g(x)^n + p m(x) in Z-poly",
    "H_2: p is a prime number",
    "H_3: g(x) is monic",
    "H_4: g(x) mod p is irreducible in Z/pZ-poly",
    "H_5: m(x) mod p is not divisible by g(x) mod p",
    "¬Q: f(x) is reducible in Q-poly"
]

N_HYP = 5
NEG_Q_INDEX = 5