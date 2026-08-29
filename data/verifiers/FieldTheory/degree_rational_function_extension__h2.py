import sympy
from sympy import Rational, Poly
from sympy.abc import t

def conditions(witness) -> list[bool]:
    try:
        K_name, p_expr, q_expr, t_val = witness
    except Exception:
        return [False, False, False, False]

    try:
        h1_ok = (K_name == "QQ")
    except Exception:
        h1_ok = False

    try:
        f_expr = sympy.cancel(p_expr / q_expr)
        h2_ok = bool(sympy.simplify(sympy.diff(f_expr, t)) != 0)
    except Exception:
        h2_ok = False

    try:
        p_poly = Poly(p_expr, t, domain='QQ')
        q_poly = Poly(q_expr, t, domain='QQ')
        gcd_poly = p_poly.gcd(q_poly)
        h3_ok = bool(gcd_poly.degree() <= 0)
    except Exception:
        h3_ok = False

    try:
        max_deg = max(p_poly.degree(), q_poly.degree())
        t_minpoly = sympy.minpoly(t_val)
        f_val = f_expr.subs(t, t_val)
        f_minpoly = sympy.minpoly(f_val)
        
        deg_t_over_Q = t_minpoly.degree()
        deg_f_over_Q = f_minpoly.degree()
        
        actual_deg = sympy.Rational(deg_t_over_Q, deg_f_over_Q)
        neg_q_ok = bool(actual_deg != max_deg)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: f is a non-constant rational function",
    "H_3: p and q are coprime polynomials",
    "¬Q: The degree of the field extension is not exactly max(deg(p), deg(q))"
]

N_HYP = 3
NEG_Q_INDEX = 3