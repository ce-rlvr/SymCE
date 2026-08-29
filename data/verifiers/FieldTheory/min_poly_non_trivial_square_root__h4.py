import sympy as sp

x = sp.Symbol('x')

def conditions(witness):
    try:
        if len(witness) == 3:
            alpha, m, beta = witness
        elif len(witness) == 4:
            _, alpha, m, beta = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]
        
    # H1: alpha is algebraic over F
    try:
        m_alpha = sp.minpoly(alpha, x)
        h1 = True
    except Exception:
        h1 = False
        
    # H2: m(x) is the minimal polynomial of alpha over F
    try:
        if isinstance(m, sp.Poly):
            m_expr = m.as_expr()
        else:
            m_expr = m
        h2 = bool(sp.simplify(m_expr - m_alpha) == 0)
    except Exception:
        h2 = False
        
    # H3: beta is an element of an extension field of F such that beta^2 = alpha
    try:
        h3 = bool(sp.simplify(beta**2 - alpha) == 0)
    except Exception:
        h3 = False
        
    # neg_Q: The minimal polynomial of beta over F is NOT m(x^2)
    try:
        m_beta = sp.minpoly(beta, x)
        m_x2 = m_expr.subs(x, x**2)
        neg_q = bool(sp.simplify(m_beta - m_x2) != 0)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: alpha is algebraic over F",
    "H_2: m(x) is the minimal polynomial of alpha over F",
    "H_3: beta is an element of an extension field of F such that beta^2 = alpha",
    "¬Q: The minimal polynomial of beta over F is not m(x^2)"
]

N_HYP = 3
NEG_Q_INDEX = 3