import sympy
from sympy import Poly, minpoly
from sympy.abc import x

# Top-level setup
# The witness expressions may reference 'x' as the polynomial variable.

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the conjecture.
    The witness is expected to be a tuple (f, g, alpha) or (F, f, g, alpha),
    where f and g are polynomials in x, and alpha is an algebraic number.
    We evaluate the conditions over the field of rational numbers (Q).
    """
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                f, g, alpha = witness
            elif len(witness) == 4:
                _, f, g, alpha = witness
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]
            
        # Ensure f and g are expressions, not Poly objects, for uniform substitution
        if hasattr(f, 'as_expr'):
            f = f.as_expr()
        if hasattr(g, 'as_expr'):
            g = g.as_expr()
    except Exception:
        return [False, False, False, False]

    # H_1: f and g are monic polynomials over Q
    try:
        f_poly = Poly(f, x, domain='QQ')
        g_poly = Poly(g, x, domain='QQ')
        h1 = (f_poly.LC() == 1) and (g_poly.LC() == 1)
    except Exception:
        h1 = False

    # H_2: alpha is an algebraic element over Q
    try:
        m_alpha = minpoly(alpha, x)
        h2 = True
    except Exception:
        h2 = False
        m_alpha = None

    # H_3: f is the minimal polynomial of g(alpha) over Q
    try:
        g_alpha = g.subs(x, alpha)
        m_g_alpha = minpoly(g_alpha, x)
        h3 = (Poly(m_g_alpha, x, domain='QQ') == Poly(f, x, domain='QQ'))
    except Exception:
        h3 = False

    # ¬Q: f(g(x)) is not the minimal polynomial of alpha over Q
    try:
        if m_alpha is None:
            neg_q = False
        else:
            f_g = f.subs(x, g)
            neg_q = (Poly(f_g, x, domain='QQ') != Poly(m_alpha, x, domain='QQ'))
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = ["H_1: f and g are monic polynomials over Q", "H_2: alpha is an algebraic element over Q", "H_3: f is the minimal polynomial of g(alpha) over Q", "¬Q: f(g(x)) is not the minimal polynomial of alpha over Q"]

N_HYP = 3
NEG_Q_INDEX = 3