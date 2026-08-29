import sympy
from sympy import symbols, resultant, Poly

def conditions(witness) -> list[bool]:
    try:
        f, g, alpha, beta, minpoly_ab = witness
        x, y = symbols('x y')
        
        f_expr = f.as_expr() if hasattr(f, 'as_expr') else f
        g_expr = g.as_expr() if hasattr(g, 'as_expr') else g
        minpoly_ab_expr = minpoly_ab.as_expr() if hasattr(minpoly_ab, 'as_expr') else minpoly_ab

        f_poly = Poly(f_expr, x)
        h1 = f_poly.is_monic and f_poly.is_irreducible and sympy.simplify(f_expr.subs(x, alpha)) == 0
    except Exception:
        h1 = False

    try:
        g_poly = Poly(g_expr, x)
        h2 = g_poly.is_monic and g_poly.is_irreducible and sympy.simplify(g_expr.subs(x, beta)) == 0
    except Exception:
        h2 = False

    try:
        m = Poly(f_expr, x).degree()
        h3 = True
    except Exception:
        h3 = False

    try:
        A_y = sympy.expand((y**m) * f_expr.subs(x, x/y))
        g_y = g_expr.subs(x, y)
        R_x = resultant(A_y, g_y, y)
        h4 = True
    except Exception:
        h4 = False

    try:
        minpoly_ab_poly = Poly(minpoly_ab_expr, x)
        is_minpoly_ab = minpoly_ab_poly.is_monic and minpoly_ab_poly.is_irreducible and sympy.simplify(minpoly_ab_expr.subs(x, alpha * beta)) == 0
        if not is_minpoly_ab:
            neg_q = False
        else:
            R_poly = Poly(R_x, x)
            rem = sympy.rem(R_poly.as_expr(), minpoly_ab_poly.as_expr(), x)
            neg_q = sympy.simplify(rem) != 0
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]

CONDITION_LABELS = ["H_1: f is the minimal polynomial of alpha", "H_2: g is the minimal polynomial of beta", "H_3: m is the degree of f", "H_4: R is the resultant of y^m f(x/y) and g(y)", "not_Q: The minimal polynomial of alpha beta does not divide R(x)"]
N_HYP = 4
NEG_Q_INDEX = 4