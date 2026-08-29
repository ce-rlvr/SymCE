import sympy as sp

x, z = sp.symbols('x z')

def get_coeff(expr, var, deg):
    p = sp.poly(expr, var)
    if p is None:
        if deg == 0:
            return expr
        return 0
    coeffs = p.all_coeffs()
    idx = len(coeffs) - 1 - deg
    if 0 <= idx < len(coeffs):
        return coeffs[idx]
    return 0

def conditions(witness):
    """
    witness is expected to be a tuple (P_expr, alpha_expr, c_expr, m_expr) or a dict
    where:
      - P_expr defines the field extension E = QQ[z]/(P_expr)
      - alpha_expr is the element alpha in E (polynomial in z)
      - c_expr is the characteristic polynomial c(x)
      - m_expr is the polynomial m(x)
    """
    try:
        if isinstance(witness, dict):
            P_expr = witness.get('P')
            alpha_expr = witness.get('alpha')
            c_expr = witness.get('c')
            m_expr = witness.get('m')
        else:
            P_expr, alpha_expr, c_expr, m_expr = witness
    except Exception:
        return [False, False, False, False]

    # H1: E/F is a finite field extension
    try:
        P_poly = sp.poly(P_expr, z, domain='QQ')
        if P_poly is None or P_poly.degree() < 1:
            h1 = False
        else:
            h1 = P_poly.is_irreducible
    except Exception:
        h1 = False

    # H2: alpha is an element of E
    try:
        alpha_poly = sp.poly(alpha_expr, z, domain='QQ')
        h2 = alpha_poly is not None
    except Exception:
        h2 = False

    # H3: c(x) is the characteristic polynomial of T(v) = alpha * v
    try:
        d = P_poly.degree()
        M_cols = []
        for i in range(d):
            prod = sp.rem(z**i * alpha_expr, P_expr, z)
            col = [get_coeff(prod, z, j) for j in range(d)]
            M_cols.append(col)
        M = sp.Matrix(M_cols).T
        char_poly = M.charpoly(x)
        c_poly = sp.poly(c_expr, x, domain='QQ')
        h3 = (c_poly is not None) and (sp.simplify(c_poly.as_expr() - char_poly.as_expr()) == 0)
    except Exception:
        h3 = False

    # neg_Q: c(x) != m(x)^deg(E over F(alpha))
    try:
        factors = sp.factor_list(char_poly.as_expr(), domain='QQ')
        if len(factors[1]) != 1:
            neg_q = False
        else:
            min_poly_expr = factors[1][0][0]
            deg_min_poly = sp.degree(min_poly_expr, x)
            deg_E = d
            index = deg_E // deg_min_poly
            
            expected_c = m_expr ** index
            neg_q = sp.simplify(c_expr - expected_c) != 0
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: E/F is a finite field extension",
    "H_2: alpha is an element of E",
    "H_3: c(x) is the characteristic polynomial of T(v) = alpha * v",
    "neg_Q: c(x) != m(x)^deg(E over F(alpha))"
]

N_HYP = 3
NEG_Q_INDEX = 3