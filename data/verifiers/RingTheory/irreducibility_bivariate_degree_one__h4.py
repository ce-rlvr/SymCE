import sympy
from sympy import Poly, factor_list, sympify
from sympy.abc import x as abc_x, y as abc_y

x, y = abc_x, abc_y

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            f, wx, wy = witness
            f = sympify(f)
            wx = sympify(wx)
            wy = sympify(wy)
        else:
            f = sympify(witness)
            wx, wy = abc_x, abc_y
    except Exception:
        return [False, False, False, False]

    try:
        p = Poly(f, wx, wy, domain='QQ')
        h1 = p.domain.is_Field
    except Exception:
        h1 = False

    try:
        p = Poly(f, wx, wy, domain='QQ')
        h2 = p.degree(wy) <= 1
    except Exception:
        h2 = False

    try:
        p = Poly(f, wx, wy, domain='QQ')
        f_expr = p.as_expr()
        g_expr = f_expr.diff(wy).subs(wy, 0)
        h_expr = f_expr.subs(wy, 0)
        pg = Poly(g_expr, wx, domain='QQ')
        ph = Poly(h_expr, wx, domain='QQ')
        gcd_gh = pg.gcd(ph)
        h3 = gcd_gh.degree() == 0 and not gcd_gh.is_zero
    except Exception:
        h3 = False

    try:
        p = Poly(f, wx, wy, domain='QQ')
        f_expr = p.as_expr()
        coeff, factors = factor_list(f_expr, domain='QQ')
        is_irreducible = (len(factors) == 1) and (factors[0][1] == 1)
        neg_q = not is_irreducible
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: f is a polynomial in x and y of degree at most 1 in y",
    "H_3: g and h are relatively prime polynomials",
    "neg_Q: f is not irreducible"
]

N_HYP = 3
NEG_Q_INDEX = 3