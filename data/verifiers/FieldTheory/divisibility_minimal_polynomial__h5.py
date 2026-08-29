import sympy
from sympy import Poly, minpoly, Dummy
from sympy.polys.domains import QQ, ZZ, RR, CC
from sympy.abc import x

def conditions(witness) -> list[bool]:
    try:
        F = witness['F']
        E = witness['E']
        alpha = witness['alpha']
        m = witness['m']
        f = witness['f']
    except Exception:
        return [False] * 5

    # H1: F is a field
    try:
        h1 = getattr(F, 'is_Field', False)
    except Exception:
        h1 = False

    # H2: E is an extension field of F
    try:
        if not getattr(E, 'is_Field', False):
            h2 = False
        else:
            try:
                unified = F.unify(E)
                h2 = (unified == E)
            except Exception:
                h2 = False
    except Exception:
        h2 = False

    # H3: alpha in E is an element algebraic over F
    try:
        try:
            val = E.from_sympy(alpha)
            in_E = True
        except Exception:
            in_E = False

        x_dummy = Dummy('x')
        mp = minpoly(alpha, x_dummy, domain=F)
        is_alg = mp is not None

        h3 = in_E and is_alg
    except Exception:
        h3 = False

    # H4: m(x) is the minimal polynomial of alpha over F
    try:
        if not isinstance(m, Poly):
            m_poly = Poly(m, x, domain=F)
        else:
            m_poly = m

        gen = m_poly.gen
        mp = minpoly(alpha, gen, domain=F)
        mp_poly = Poly(mp, gen, domain=F)
        h4 = (m_poly.domain == F) and (m_poly == mp_poly)
    except Exception:
        h4 = False

    # neg_Q: m(x) does not divide f(x)
    try:
        if not isinstance(m, Poly):
            m_poly = Poly(m, x, domain=F)
        else:
            m_poly = m

        if not isinstance(f, Poly):
            f_poly = Poly(f, m_poly.gen, domain=F)
        else:
            f_poly = f

        if f_poly.domain == F and m_poly.domain == F:
            rem = f_poly % m_poly
            neg_q = not rem.is_zero
        else:
            neg_q = True
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: E is an extension field of F",
    "H_3: alpha in E is an element algebraic over F",
    "H_4: m(x) is the minimal polynomial of alpha over F",
    "neg_Q: m(x) does not divide f(x)"
]

N_HYP = 4
NEG_Q_INDEX = 4