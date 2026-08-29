import sympy as sp

CONDITION_LABELS = [
    "H_1: alpha is algebraic over F",
    "H_2: beta is an element of an extension field of F such that beta^2 = alpha",
    "H_3: beta is not an element of F(alpha)",
    "¬Q: The minimal polynomial of beta over F is not m(x^2)"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    """
    witness is expected to be a tuple: (alpha, beta)
    where alpha and beta are algebraic numbers (sympy expressions).
    The base field F is taken to be the rationals QQ.
    """
    try:
        alpha, beta = witness
    except Exception:
        return [False, False, False, False]

    # H_1: alpha is algebraic over F (QQ)
    try:
        m_alpha = sp.minpoly(alpha, polys=True)
        h1_ok = m_alpha is not None and m_alpha.degree() > 0
    except Exception:
        h1_ok = False

    # H_2: beta is an element of an extension field of F such that beta^2 = alpha
    try:
        m_beta = sp.minpoly(beta, polys=True)
        is_algebraic = m_beta is not None and m_beta.degree() > 0
        # Check if beta^2 == alpha
        diff = sp.simplify(beta**2 - alpha)
        h2_ok = is_algebraic and (diff == 0)
    except Exception:
        h2_ok = False

    # H_3: beta is not an element of F(alpha)
    try:
        # If beta is in QQ(alpha), then its degree over QQ must divide the degree of alpha over QQ.
        # Since beta^2 = alpha, if beta is in QQ(alpha), QQ(beta) = QQ(alpha), so they have the same degree.
        # If beta is NOT in QQ(alpha), the degree of beta over QQ will be 2 * degree of alpha over QQ.
        deg_alpha = m_alpha.degree()
        deg_beta = m_beta.degree()
        h3_ok = (deg_beta > deg_alpha)
    except Exception:
        h3_ok = False

    # ¬Q: The minimal polynomial of beta over F is not m(x^2)
    try:
        x = sp.Symbol('x')
        m_alpha_expr = m_alpha.as_expr(x)
        m_x2_expr = m_alpha_expr.subs(x, x**2)
        m_beta_expr = m_beta.as_expr(x)
        
        # Check if m_beta(x) == m_alpha(x^2)
        diff_poly = sp.simplify(m_beta_expr - m_x2_expr)
        neg_q_ok = (diff_poly != 0)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]