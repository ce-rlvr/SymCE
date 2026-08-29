import sympy
from sympy import Symbol, Poly, CRootOf, minpoly, factor_list
from sympy.abc import x, y

# Top-level setup
# F is implicitly the rational field QQ. 
# E is represented as QQ[x]/<theta_poly_expr>.
# alpha is represented as alpha_poly_expr evaluated at the generator of E.

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple: (theta_poly_expr, alpha_poly_expr)
    where:
      - theta_poly_expr is an irreducible polynomial in x over QQ defining the extension E.
      - alpha_poly_expr is a polynomial in x over QQ representing alpha in E.
    """
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False, False]
        theta_poly_expr = sympy.sympify(witness[0])
        alpha_poly_expr = sympy.sympify(witness[1])
    except Exception:
        return [False, False, False]
        
    # H_1: E/F is an algebraic field extension
    try:
        p_theta = Poly(theta_poly_expr, x, domain='QQ')
        h1 = bool(p_theta.degree() > 0 and p_theta.is_irreducible)
    except Exception:
        h1 = False
        
    # H_2: alpha is an element of E
    try:
        p_alpha = Poly(alpha_poly_expr, x, domain='QQ')
        h2 = True
    except Exception:
        h2 = False
        
    # neg_Q: The minimal polynomial of alpha over F does NOT factor completely into linear polynomials over E
    try:
        theta = CRootOf(theta_poly_expr, 0)
        alpha_val = alpha_poly_expr.subs(x, theta)
        
        mp_alt = minpoly(alpha_val, y)
        
        factors = factor_list(mp_alt, extension=theta)
        
        all_linear = True
        for factor_expr, mult in factors[1]:
            deg = Poly(factor_expr, y).degree()
            if deg > 1:
                all_linear = False
                break
                
        neg_q = not all_linear
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: E/F is an algebraic field extension",
    "H_2: alpha is an element of E",
    "¬Q: The minimal polynomial of alpha over F does not factor completely into linear polynomials over E"
]

N_HYP = 2
NEG_Q_INDEX = 2