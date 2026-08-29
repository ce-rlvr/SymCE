import sympy as sp
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import Poly
from sympy.abc import x, t

Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
V4 = AlternatingGroup(4)
trivial = CyclicGroup(1)
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: E/F is a finite field extension",
    "H_2: alpha is an element of E",
    "H_3: m(x) is the minimal polynomial of alpha over F",
    "not Q: c(x) != m(x)**deg(E/F(alpha))"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if len(witness) != 4:
            return [False, False, False, False]
        min_poly_E_expr, alpha_poly_expr, m_poly_expr, c_poly_expr = witness
    except Exception:
        return [False, False, False, False]

    try:
        domain = 'QQ'
        for expr in witness:
            if isinstance(expr, Poly):
                domain = expr.domain
                break
                
        min_poly_E = Poly(min_poly_E_expr, t, domain=domain)
        alpha_poly = Poly(alpha_poly_expr, t, domain=domain)
        m_poly = Poly(m_poly_expr, x, domain=domain)
        c_poly = Poly(c_poly_expr, x, domain=domain)
    except Exception:
        return [False, False, False, False]

    try:
        h1 = min_poly_E.degree() >= 1 and min_poly_E.is_irreducible
    except Exception:
        h1 = False

    try:
        h2 = True
    except Exception:
        h2 = False

    try:
        if not m_poly.is_monic:
            h3 = False
        elif not m_poly.is_irreducible:
            h3 = False
        else:
            composed_expr = m_poly.as_expr().subs(x, alpha_poly.as_expr())
            rem = Poly(composed_expr, t, domain=domain) % min_poly_E
            h3 = rem.is_zero
    except Exception:
        h3 = False

    try:
        deg_E = min_poly_E.degree()
        deg_F_alpha = m_poly.degree()
        if deg_F_alpha == 0 or deg_E % deg_F_alpha != 0:
            neg_q = True
        else:
            idx = deg_E // deg_F_alpha
            expected_c = m_poly ** idx
            neg_q = (c_poly != expected_c)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]