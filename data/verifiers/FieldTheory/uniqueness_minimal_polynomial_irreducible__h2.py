import sympy

x = sympy.Symbol('x')

def conditions(witness) -> list[bool]:
    try:
        F, alpha, p = witness
    except Exception:
        return [False] * 6

    try:
        h1 = F.is_Field
    except Exception:
        h1 = False

    try:
        m_poly = sympy.minpoly(alpha, x, domain=F)
        h2 = m_poly is not None
    except Exception:
        h2 = False

    try:
        h3 = (p.domain == F) and p.is_monic
    except Exception:
        h3 = False

    try:
        h4 = p.is_irreducible
    except Exception:
        h4 = False

    try:
        val = p.eval(alpha)
        h5 = (sympy.simplify(val) == 0)
    except Exception:
        h5 = False

    try:
        m_poly = sympy.minpoly(alpha, x, domain=F)
        m_poly_obj = sympy.Poly(m_poly, x, domain=F)
        neg_q = (p != m_poly_obj)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(h5), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: alpha is an element algebraic over F",
    "H_3: p is a monic polynomial over F",
    "H_4: p is irreducible over F",
    "H_5: p(alpha) = 0",
    "not Q: p is not the minimal polynomial of alpha over F"
]

N_HYP = 5
NEG_Q_INDEX = 5