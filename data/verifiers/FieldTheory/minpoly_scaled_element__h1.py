import sympy as sp
from sympy import symbols, Rational, minpoly

# Top-level setup
x = symbols('x')

def conditions(witness) -> list[bool]:
    """
    witness is expected to be a tuple: (alpha, c, m, n)
    where:
      - alpha is the algebraic element
      - c is the non-zero element in F
      - m is the minimal polynomial of alpha over F (as a SymPy expression in x)
      - n is the degree of m
    """
    try:
        alpha, c, m, n = witness
    except Exception:
        return [False, False, False]

    # H_1: alpha is algebraic over F with minimal polynomial m(x) of degree n
    try:
        # We check if m(alpha) == 0 and the degree of m is n
        # For simplicity, we assume F is the field of rational numbers (or a subfield)
        # and check if m is irreducible and monic (standard minimal polynomial properties over Q)
        m_expr = sp.sympify(m)
        is_root = sp.simplify(m_expr.subs(x, alpha)) == 0
        is_deg_n = sp.degree(m_expr, x) == n
        is_monic = sp.LC(m_expr, x) == 1
        is_irreducible = sp.polys.polytools.is_irreducible(m_expr, domain='QQ')
        h1_ok = bool(is_root and is_deg_n and is_irreducible)
    except Exception:
        h1_ok = False

    # H_2: c in F is a non-zero element
    try:
        # We check if c is non-zero and rational (in F = QQ)
        c_val = sp.sympify(c)
        h2_ok = bool(c_val != 0 and c_val.is_rational)
    except Exception:
        h2_ok = False

    # ¬Q: The minimal polynomial of c*alpha over F is NOT given by c^n * m(x/c)
    try:
        # Calculate the proposed polynomial P(x) = c^n * m(x/c)
        proposed_poly = sp.simplify(c_val**n * m_expr.subs(x, x / c_val))
        
        # Calculate the actual minimal polynomial of c*alpha over Q
        actual_minpoly = minpoly(c_val * alpha, x)
        
        # The conclusion fails if the proposed polynomial is NOT the actual minimal polynomial
        neg_q_ok = bool(sp.simplify(proposed_poly - actual_minpoly) != 0)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: alpha is algebraic over F with minimal polynomial m(x) of degree n",
    "H_2: c in F is a non-zero element",
    "¬Q: The minimal polynomial of c*alpha over F is NOT given by c^n * m(x/c)"
]

N_HYP = 2
NEG_Q_INDEX = 2