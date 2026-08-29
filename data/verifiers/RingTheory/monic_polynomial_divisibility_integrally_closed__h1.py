import sympy
from sympy import Poly, sympify, div, cancel
from sympy.abc import x, y, z, a, b, c

def conditions(witness):
    try:
        R, K, f_expr, g_expr, x_var = witness
    except Exception:
        return [False, False, False, False]

    try:
        h1 = bool(K == R.get_field())
    except Exception:
        h1 = False

    def in_R(expr):
        try:
            R.from_sympy(cancel(sympify(expr)))
            return True
        except Exception:
            return False

    try:
        f_poly = Poly(f_expr, x_var)
        g_poly = Poly(g_expr, x_var)
        f_coeffs_in_R = all(in_R(c_val) for c_val in f_poly.coeffs())
        g_coeffs_in_R = all(in_R(c_val) for c_val in g_poly.coeffs())
        f_monic = (f_poly.LC() == 1)
        g_monic = (g_poly.LC() == 1)
        h2 = bool(f_coeffs_in_R and g_coeffs_in_R and f_monic and g_monic)
    except Exception:
        h2 = False

    try:
        q_K, r_K = div(g_expr, f_expr, x_var, domain=K)
        h3 = bool(r_K == 0)
    except Exception:
        h3 = False

    try:
        if not h3:
            neg_q = True
        else:
            q_poly = Poly(q_K, x_var)
            q_coeffs_in_R = all(in_R(c_val) for c_val in q_poly.coeffs())
            neg_q = not bool(q_coeffs_in_R)
    except Exception:
        neg_q = True

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: K is the field of fractions of R",
    "H_2: f and g are monic polynomials over R",
    "H_3: f divides g in the polynomial ring over K",
    "not Q: f does not divide g in the polynomial ring over R"
]

N_HYP = 3
NEG_Q_INDEX = 3