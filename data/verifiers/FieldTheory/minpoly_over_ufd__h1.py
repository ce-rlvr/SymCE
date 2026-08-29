import sympy as sp

x = sp.Symbol('x')

def check_Z_span(expr, basis, coeffs):
    if len(basis) != len(coeffs): return False
    for c in coeffs:
        if not sp.sympify(c).is_integer:
            return False
    expected = sum(sp.sympify(c) * b for c, b in zip(coeffs, basis))
    return sp.simplify(expr - expected) == 0

def check_Q_span(expr, basis, coeffs):
    if len(basis) != len(coeffs): return False
    for c in coeffs:
        if not sp.sympify(c).is_rational:
            return False
    expected = sum(sp.sympify(c) * b for c, b in zip(coeffs, basis))
    return sp.simplify(expr - expected) == 0

def conditions(witness) -> list[bool]:
    try:
        w_x = witness['x']
        alpha = witness['alpha']
        R_basis = witness['R_basis']
        R_basis_1_coeffs = witness['R_basis_1_coeffs']
        R_basis_mul_coeffs = witness['R_basis_mul_coeffs']
        integral_poly = witness['integral_poly']
        integral_poly_coeffs = witness['integral_poly_coeffs']
        min_poly_F = witness['min_poly_F']
        min_poly_F_coeffs = witness['min_poly_F_coeffs']
    except Exception:
        return [False, False, False, False]

    # H1: F is the field of fractions of R
    try:
        h1 = False
        if len(R_basis) == 2:
            ratio = sp.simplify(R_basis[1] / R_basis[0])
            if not ratio.is_rational:
                if check_Z_span(sp.Integer(1), R_basis, R_basis_1_coeffs):
                    closed = True
                    for i in range(2):
                        for j in range(2):
                            prod = R_basis[i] * R_basis[j]
                            if not check_Z_span(prod, R_basis, R_basis_mul_coeffs[(i, j)]):
                                closed = False
                    if closed:
                        h1 = True
    except Exception:
        h1 = False

    # H2: E is a field extension of F
    try:
        h2 = isinstance(alpha, sp.Expr)
    except Exception:
        h2 = False

    # H3: alpha is integral over R
    try:
        h3 = False
        poly_int = sp.Poly(integral_poly, w_x)
        if poly_int.LC() == 1:
            if sp.simplify(integral_poly.subs(w_x, alpha)) == 0:
                coeffs_int = poly_int.all_coeffs()
                if len(coeffs_int) == len(integral_poly_coeffs):
                    all_in_R = True
                    for c_expr, c_Z in zip(coeffs_int, integral_poly_coeffs):
                        if not check_Z_span(c_expr, R_basis, c_Z):
                            all_in_R = False
                    if all_in_R:
                        h3 = True
    except Exception:
        h3 = False

    # neg_Q: The minimal polynomial of alpha over F does not have all its coefficients in R
    try:
        neg_q = False
        poly_min = sp.Poly(min_poly_F, w_x)
        if poly_min.degree() == 1 and poly_min.LC() == 1:
            if sp.simplify(min_poly_F.subs(w_x, alpha)) == 0:
                coeffs_min = poly_min.all_coeffs()
                if len(coeffs_min) == len(min_poly_F_coeffs):
                    all_in_F = True
                    all_in_R = True
                    for c_expr, c_Q in zip(coeffs_min, min_poly_F_coeffs):
                        if not check_Q_span(c_expr, R_basis, c_Q):
                            all_in_F = False
                        for q_val in c_Q:
                            if not sp.sympify(q_val).is_integer:
                                all_in_R = False
                    if all_in_F and not all_in_R:
                        neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is the field of fractions of R",
    "H_2: E is a field extension of F",
    "H_3: alpha is integral over R",
    "¬Q: The minimal polynomial of alpha over F does not have all its coefficients in R"
]

N_HYP = 3
NEG_Q_INDEX = 3