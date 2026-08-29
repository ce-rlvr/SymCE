import sympy as sp
from sympy import Poly

x = sp.Symbol('x')
ZZ = sp.S.Integers
QQ = sp.S.Rationals

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                f, g = witness
            elif len(witness) == 4:
                _, _, f, g = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    try:
        f_poly = Poly(f, x)
        g_poly = Poly(g, x)
        h1 = all(c.is_integer for c in f_poly.coeffs()) and all(c.is_integer for c in g_poly.coeffs())
    except Exception:
        h1 = False

    h2 = h1

    try:
        q_QQ, r_QQ = sp.div(g, f, domain='QQ')
        h3 = (r_QQ == 0)
    except Exception:
        h3 = False

    try:
        if not h3:
            neg_q = False
        else:
            q_poly = Poly(q_QQ, x)
            divides_in_ZZ = all(c.is_integer for c in q_poly.coeffs())
            neg_q = not divides_in_ZZ
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is an integrally closed integral domain",
    "H_2: K is the field of fractions of R",
    "H_3: f divides g in polynomial ring over K",
    "¬Q: f does not divide g in polynomial ring over R"
]

N_HYP = 3
NEG_Q_INDEX = 3