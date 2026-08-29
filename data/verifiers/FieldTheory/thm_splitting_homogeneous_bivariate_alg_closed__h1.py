import sympy
from sympy.abc import x, y

def conditions(witness):
    try:
        expr = sympy.sympify(witness)
        if not expr.free_symbols.issubset({x, y}):
            h1 = False
        else:
            poly = sympy.Poly(expr, x, y)
            d = poly.total_degree()
            h1 = bool(poly.is_homogeneous and d >= 1)
    except Exception:
        h1 = False

    try:
        expr = sympy.sympify(witness)
        coeff, factors = sympy.factor_list(expr)
        if coeff == 0:
            neg_q = True
        else:
            all_linear_homog = True
            for f, mult in factors:
                f_poly = sympy.Poly(f, x, y)
                if f_poly.total_degree() != 1 or not f_poly.is_homogeneous:
                    all_linear_homog = False
                    break
            neg_q = not all_linear_homog
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = ["H_1: F(x, y) is a homogeneous polynomial of degree d >= 1", "not Q: F(x, y) does not factor into a product of a non-zero constant and d linear homogeneous polynomials"]
N_HYP = 1
NEG_Q_INDEX = 1