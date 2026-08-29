import sympy as sp
from sympy import minpoly, Poly
from sympy.abc import x, y, z

QQ = sp.QQ
ZZ = sp.ZZ

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple or dict providing:
    (alpha, c, m, x_var, domain)
    where:
      - alpha: an algebraic element in E
      - c: an element to shift by (in E, but not necessarily in F)
      - m: the minimal polynomial of alpha over F
      - x_var: the variable used in m
      - domain: the base field F (e.g., QQ)
    """
    try:
        if isinstance(witness, dict):
            alpha = witness['alpha']
            c = witness['c']
            m = witness['m']
            x_var = witness['x']
            domain = witness['domain']
        else:
            alpha, c, m, x_var, domain = witness
    except Exception:
        return [False, False, False]

    # H1: F is a field and E/F is a field extension
    try:
        h1 = getattr(domain, 'is_Field', False)
        h1 = h1 and isinstance(alpha, sp.Expr) and isinstance(c, sp.Expr)
    except Exception:
        h1 = False

    # H2: alpha is algebraic over F with minimal polynomial m(x)
    try:
        m_expr = m.as_expr() if isinstance(m, Poly) else m
        poly_m = Poly(m_expr, x_var, domain=domain)
        is_monic = poly_m.LC() == 1
        actual_minpoly = minpoly(alpha, x_var, domain=domain)
        h2 = is_monic and sp.simplify(actual_minpoly - m_expr) == 0
    except Exception:
        h2 = False

    # neg_Q: The minimal polynomial of alpha + c over F is NOT m(x - c)
    try:
        actual_minpoly_ac = minpoly(alpha + c, x_var, domain=domain)
        expected_m = m_expr.subs(x_var, x_var - c)
        neg_q = sp.simplify(actual_minpoly_ac - expected_m) != 0
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a field and E/F is a field extension",
    "H_2: alpha is algebraic over F with minimal polynomial m(x)",
    "¬Q: The minimal polynomial of alpha + c over F is not m(x - c)"
]

N_HYP = 2
NEG_Q_INDEX = 2