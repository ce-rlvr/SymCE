import sympy
from sympy import Symbol, Poly, simplify, minpoly

x = Symbol('x')

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                F, alpha, m = witness
            elif len(witness) == 2:
                if isinstance(witness[0], Poly):
                    m, alpha = witness[0], witness[1]
                elif isinstance(witness[1], Poly):
                    alpha, m = witness[0], witness[1]
                else:
                    if 'x' in str(witness[0]) and 'x' not in str(witness[1]):
                        m, alpha = witness[0], witness[1]
                    else:
                        alpha, m = witness[0], witness[1]
            else:
                return [False] * 5
        else:
            return [False] * 5

        alpha = sympy.sympify(alpha)

        if isinstance(m, Poly):
            m_expr = m.as_expr()
            if m.gens:
                m_expr = m_expr.subs(m.gens[0], x)
            n = m.degree()
        else:
            m_expr = sympy.sympify(m)
            free = m_expr.free_symbols
            if free:
                var = list(free)[0]
                m_expr = m_expr.subs(var, x)
            m_poly = Poly(m_expr, x)
            n = m_poly.degree()
            
    except Exception:
        return [False] * 5

    # H1: alpha is algebraic over a field F
    try:
        kwargs = {}
        if 'F' in locals() and F is not None and hasattr(F, 'get_ring'):
            kwargs['domain'] = F
        mp = minpoly(alpha, x, **kwargs)
        h1 = True
    except Exception:
        h1 = False

    # H2: m(x) satisfies the reciprocal property x^n m(1/x) = m(x)
    try:
        if n < 0:
            h2 = False
        else:
            recip = sympy.expand(x**n * m_expr.subs(x, 1/x))
            h2 = bool(sympy.simplify(recip - m_expr) == 0)
    except Exception:
        h2 = False

    # H3: alpha != 1
    try:
        h3 = bool(sympy.simplify(alpha - 1) != 0)
    except Exception:
        h3 = False

    # H4: alpha != -1
    try:
        h4 = bool(sympy.simplify(alpha + 1) != 0)
    except Exception:
        h4 = False

    # neg_Q: The minimal polynomial of alpha + alpha^{-1} over F does NOT have degree n/2
    try:
        beta = sympy.simplify(alpha + 1/alpha)
        kwargs = {}
        if 'F' in locals() and F is not None and hasattr(F, 'get_ring'):
            kwargs['domain'] = F
        minpoly_beta = minpoly(beta, x, **kwargs)
        deg_beta = Poly(minpoly_beta, x).degree()
        neg_q = bool(deg_beta != n / 2)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: alpha is algebraic over a field F",
    "H_2: m(x) satisfies the reciprocal property x^n m(1/x) = m(x)",
    "H_3: alpha != 1",
    "H_4: alpha != -1",
    "¬Q: The minimal polynomial of alpha + alpha^{-1} over F does not have degree n/2"
]

N_HYP = 4
NEG_Q_INDEX = 4