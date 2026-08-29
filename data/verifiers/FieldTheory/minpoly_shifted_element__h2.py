import sympy
from sympy import Symbol, Rational
from sympy.polys.numberfields import minpoly

# Top-level setup
x = Symbol('x')

def conditions(witness):
    """
    Checks the remaining hypotheses and the negated conclusion.
    The witness is expected to be a tuple (m, c, alpha) or a dictionary
    with keys 'm', 'c', 'alpha', where:
      - m is a sympy expression in x (the proposed minimal polynomial of alpha)
      - c is a rational number (element of the base field F = Q)
      - alpha is an algebraic number (element of the extension field E)
    """
    try:
        if isinstance(witness, dict):
            m = witness.get('m', x)
            c = witness.get('c', Rational(0))
            alpha = witness.get('alpha', Rational(0))
        else:
            m, c, alpha = witness
    except Exception:
        return [False, False, False]

    # H_1: F is a field and E/F is a field extension
    # We work over F = Q. Any valid sympy expression for alpha can be considered 
    # to live in some extension E/Q.
    try:
        alpha_val = sympy.sympify(alpha)
        h1 = isinstance(alpha_val, sympy.Expr)
    except Exception:
        h1 = False

    # H_2: c in F is an element of the base field
    # We check if c is a rational number (since F = Q)
    try:
        c_val = sympy.sympify(c)
        h2 = c_val.is_rational is True
    except Exception:
        h2 = False

    # neg_Q: The minimal polynomial of alpha + c over F is NOT m(x - c)
    try:
        m_expr = sympy.sympify(m)
        if isinstance(m_expr, sympy.Poly):
            m_expr = m_expr.as_expr()
        
        # Compute the actual minimal polynomial of alpha + c over Q
        actual_minpoly = minpoly(alpha_val + c_val, x)
        actual_p = sympy.Poly(actual_minpoly, x)
        actual_monic = sympy.expand(actual_minpoly / actual_p.LC())
        
        # Compute m(x - c)
        expected_minpoly = m_expr.subs(x, x - c_val)
        expected_p = sympy.Poly(expected_minpoly, x)
        
        if expected_p.is_zero:
            neg_q = True
        else:
            expected_monic = sympy.expand(expected_minpoly / expected_p.LC())
            diff = sympy.simplify(actual_monic - expected_monic)
            neg_q = bool(diff != 0)
    except Exception:
        # If minpoly fails (e.g., alpha is not algebraic) or m is not a polynomial,
        # then the conclusion that the minimal polynomial is m(x-c) is false.
        neg_q = True

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field and E/F is a field extension",
    "H_2: c in F is an element of the base field",
    "¬Q: The minimal polynomial of alpha + c over F is not m(x - c)"
]

N_HYP = 2
NEG_Q_INDEX = 2