import sympy as sp
from sympy import Poly, degree
from sympy.abc import x, z
from sympy.ntheory import totient
from sympy.polys import cyclotomic_poly

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f(x) is an irreducible separable polynomial over F",
    "H_3: Gal(E/F) is an abelian group",
    "H_4: alpha in E is a root of f(x)",
    "not Q: F(alpha) is not equal to the splitting field E"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness):
    try:
        n, f_expr, alpha_expr = witness
        if not isinstance(n, int) or n < 1:
            return [False] * 5
    except Exception:
        return [False] * 5

    # H_1: F is a field
    h1 = True

    # H_2: f(x) is an irreducible separable polynomial over F
    try:
        f_poly = Poly(f_expr, x, domain='QQ')
        h2 = f_poly.is_irreducible
    except Exception:
        h2 = False

    # H_3: Gal(E/F) is an abelian group
    h3 = True

    # H_4: alpha in E is a root of f(x)
    try:
        alpha_p = Poly(alpha_expr, z, domain='QQ')
        f_alpha_expr = f_expr.subs(x, alpha_expr)
        f_alpha_p = Poly(f_alpha_expr, z, domain='QQ')
        cyclo_p = cyclotomic_poly(n, z)
        _, rem = f_alpha_p.div(cyclo_p)
        h4 = rem.is_zero
    except Exception:
        h4 = False

    # not Q: F(alpha) is not equal to the splitting field E
    try:
        deg_f = degree(f_expr, x)
        deg_E = totient(n)
        neg_q = (deg_f != deg_E)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]