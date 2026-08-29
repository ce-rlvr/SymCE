import sympy
from sympy.abc import x

def conditions(witness):
    try:
        if len(witness) != 4:
            return [False, False, False]
        a, b, m, P = witness
    except Exception:
        return [False, False, False]

    try:
        a_sym = sympy.sympify(a)
        b_sym = sympy.sympify(b)
        m_sym = sympy.sympify(m)
        h1 = bool(a_sym.is_integer and b_sym.is_integer and m_sym.is_integer and m_sym > 0)
    except Exception:
        h1 = False

    try:
        h2 = bool((a_sym - b_sym) % m_sym == 0)
    except Exception:
        h2 = False

    try:
        P_expr = sympy.sympify(P)
        if isinstance(P_expr, sympy.Poly):
            P_expr = P_expr.as_expr()
            
        if not P_expr.is_polynomial(x) or not P_expr.free_symbols.issubset({x}):
            neg_q = False
        else:
            pa = P_expr.subs(x, a_sym)
            pb = P_expr.subs(x, b_sym)
            diff = sympy.simplify(pa - pb)
            quotient = sympy.simplify(diff / m_sym)
            neg_q = not bool(quotient.is_integer)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a, b, m are integers with m > 0",
    "H_2: a == b (mod m)",
    "¬Q: P(a) != P(b) (mod m)"
]

N_HYP = 2
NEG_Q_INDEX = 2