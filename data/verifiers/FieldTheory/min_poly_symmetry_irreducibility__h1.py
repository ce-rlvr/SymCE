import sympy
from sympy import minpoly, degree, pi, sqrt, I, Rational
from sympy.polys.numberfields import primitive_element
from sympy.abc import x, y, z

# Top-level setup
# No specific named objects required for this FieldTheory conjecture,
# but we provide standard symbols and constants.

def is_minpoly_irreducible(u, v):
    """
    Checks if the minimal polynomial of u over Q is irreducible in Q(v) polynomials.
    Returns False if u is not algebraic (minimal polynomial doesn't exist).
    """
    try:
        poly_u = minpoly(u)
        deg_u = degree(poly_u)
    except Exception:
        return False
        
    try:
        poly_v = minpoly(v)
        deg_v = degree(poly_v)
        v_is_alg = True
    except Exception:
        v_is_alg = False
        
    if not v_is_alg:
        # If v is transcendental, the minimal polynomial of u over Q 
        # remains irreducible over Q(v) because Q is algebraically closed in Q(v).
        return True
        
    try:
        # Both are algebraic. The minimal polynomial of u over Q is irreducible 
        # over Q(v) iff [Q(u, v) : Q] == [Q(u) : Q] * [Q(v) : Q]
        elem, poly = primitive_element([u, v], ex=True)
        deg_uv = degree(poly)
        return deg_uv == deg_u * deg_v
    except Exception:
        pass

    # Fallback if primitive_element fails
    for c in range(1, 10):
        try:
            poly_uv = minpoly(u + c*v)
            if degree(poly_uv) == deg_u * deg_v:
                return True
        except Exception:
            pass
            
    return False

def conditions(witness):
    try:
        alpha, beta = witness
    except Exception:
        return [False, False]
        
    try:
        # H_1: beta is algebraic over F
        minpoly(beta)
        h1_ok = True
    except Exception:
        h1_ok = False
        
    try:
        # Conclusion: The minimal polynomial of alpha over F is irreducible in F(beta) polynomials 
        # if and only if the minimal polynomial of beta over F is irreducible in F(alpha) polynomials
        p_alpha = is_minpoly_irreducible(alpha, beta)
        p_beta = is_minpoly_irreducible(beta, alpha)
        
        # The conclusion fails if the two truth values are not equal
        neg_q_ok = (p_alpha != p_beta)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = ["H_1: beta is algebraic over F", "not Q: minpoly of alpha over F is irreducible over F(beta) iff minpoly of beta over F is irreducible over F(alpha)"]

N_HYP = 1
NEG_Q_INDEX = 1