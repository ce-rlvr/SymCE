import sympy
from sympy import Poly
from sympy.abc import x

def conditions(witness):
    """
    Check the hypotheses and the negated conclusion for the conjecture:
    "If F is a field, f(x) and g(x) are non-constant polynomials, and f(g(x)) is irreducible in F[x],
    then f(x) is irreducible in F[x]."
    """
    try:
        # Parse the witness
        if isinstance(witness, dict):
            domain = witness.get('domain', sympy.QQ)
            f_expr = witness['f']
            g_expr = witness['g']
        elif isinstance(witness, (list, tuple)) and len(witness) == 3:
            domain, f_expr, g_expr = witness
        elif isinstance(witness, (list, tuple)) and len(witness) == 2:
            f_expr, g_expr = witness
            domain = sympy.QQ
        else:
            return [False, False, False, False]
            
        # Handle string domain representations
        if isinstance(domain, str):
            if domain == 'QQ':
                domain = sympy.QQ
            elif domain == 'ZZ':
                domain = sympy.ZZ
            elif domain == 'RR':
                domain = sympy.RR
            elif domain == 'CC':
                domain = sympy.CC
                
        # Ensure f and g are SymPy expressions
        if isinstance(f_expr, Poly):
            f_expr = f_expr.as_expr()
        else:
            f_expr = sympy.sympify(f_expr)
            
        if isinstance(g_expr, Poly):
            g_expr = g_expr.as_expr()
        else:
            g_expr = sympy.sympify(g_expr)
            
    except Exception:
        return [False, False, False, False]

    # H_1: F is a field
    try:
        h1 = bool(domain.is_Field)
    except Exception:
        h1 = False

    # H_2: Both f(x) and g(x) are non-constant polynomials
    try:
        f_poly = Poly(f_expr, x)
        g_poly = Poly(g_expr, x)
        h2 = bool(f_poly.degree() >= 1 and g_poly.degree() >= 1)
    except Exception:
        h2 = False

    # H_3: The composed polynomial f(g(x)) is irreducible over F
    try:
        fg_expr = sympy.expand(f_expr.subs(x, g_expr))
        fg_poly = Poly(fg_expr, x, domain=domain)
        irr = fg_poly.is_irreducible
        h3 = True if irr is True else False
    except Exception:
        h3 = False

    # ¬Q: The polynomial f(x) is NOT irreducible over F
    try:
        f_poly_domain = Poly(f_expr, x, domain=domain)
        irr = f_poly_domain.is_irreducible
        neg_q = False if irr is None else not irr
    except Exception:
        # If f(x) cannot be constructed over F (e.g., coefficients not in F),
        # then it is not irreducible in F[x]. Thus the conclusion fails, making ¬Q True.
        neg_q = True

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: Both f(x) and g(x) are non-constant polynomials",
    "H_3: The composed polynomial f(g(x)) is irreducible over F",
    "¬Q: The polynomial f(x) is not irreducible over F"
]

N_HYP = 3
NEG_Q_INDEX = 3