import sympy
from sympy import minpoly, Poly, QQ, sympify, primitive_element
from sympy.abc import x

# Top-level setup
# The field F is implicitly taken to be the field of rational numbers (QQ).
# Witnesses should be provided as a tuple: (alpha, m, beta)
# where alpha and beta are algebraic numbers, and m is a SymPy expression or Poly.

def conditions(witness) -> list[bool]:
    try:
        alpha, m, beta = witness
    except Exception:
        return [False, False, False, False]
    
    # Extract expression for m in terms of x
    try:
        if isinstance(m, Poly):
            m_expr = m.as_expr()
        else:
            m_expr = sympify(m)
            
        if hasattr(m_expr, 'free_symbols') and len(m_expr.free_symbols) == 1:
            var = list(m_expr.free_symbols)[0]
            m_expr = m_expr.subs(var, x)
    except Exception:
        m_expr = m

    # H1: alpha is algebraic over F (QQ)
    try:
        mp_alpha = minpoly(alpha, x)
        h1 = True
    except Exception:
        h1 = False

    # H2: m(x) is the minimal polynomial of alpha over F (QQ)
    try:
        p_m = Poly(m_expr, x, domain=QQ)
        p_mp_alpha = Poly(mp_alpha, x, domain=QQ)
        h2 = p_m.monic() == p_mp_alpha.monic()
    except Exception:
        h2 = False

    # H3: beta is not an element of F(alpha)
    # We check this by verifying that the degree of Q(alpha, beta) over Q 
    # is strictly greater than the degree of Q(alpha) over Q.
    try:
        _, mp_ext = primitive_element([alpha, beta], x, polys=True)
        deg_ext = mp_ext.degree()
        deg_alpha = p_mp_alpha.degree()
        h3 = deg_ext > deg_alpha
    except Exception:
        h3 = False

    # neg_Q: The minimal polynomial of beta over F is NOT m(x^2)
    try:
        p_mp_beta = Poly(minpoly(beta, x), x, domain=QQ)
        p_m_x2 = Poly(m_expr.subs(x, x**2), x, domain=QQ)
        neg_q = p_mp_beta.monic() != p_m_x2.monic()
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: alpha is algebraic over F",
    "H_2: m(x) is the minimal polynomial of alpha over F",
    "H_3: beta is not an element of F(alpha)",
    "¬Q: The minimal polynomial of beta over F is not m(x^2)"
]

N_HYP = 3
NEG_Q_INDEX = 3