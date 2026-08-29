import sympy
from sympy import Dummy, QQ, minpoly, degree, sqrt, I, Rational
from sympy.abc import x

# Top-level setup
# Provide some basic named objects that might be used in a witness
Z2 = sympy.CyclicGroup(2) if hasattr(sympy, 'CyclicGroup') else None
Z3 = sympy.CyclicGroup(3) if hasattr(sympy, 'CyclicGroup') else None

def conditions(witness):
    """
    Checks the witness for the conjecture:
    "If \alpha \in L is algebraic over K, then the degree of the minimal polynomial 
    of \alpha over M is less than or equal to the degree of the minimal polynomial 
    of \alpha over K."
    
    The conjecture is FALSE because the hypothesis that M is an intermediate field 
    (i.e., K \subseteq M) was dropped.
    
    Expected witness format:
    A tuple (alpha, K_gens, M_gens) where:
      - alpha is a sympy Expr representing the algebraic element.
      - K_gens is a list/tuple of sympy Expr representing generators of K over QQ.
      - M_gens is a list/tuple of sympy Expr representing generators of M over QQ.
    """
    try:
        alpha, K_gens, M_gens = witness
    except Exception:
        return [False, False]
        
    x_dummy = Dummy('x')
    
    # H_1: alpha is algebraic over K
    try:
        K_domain = QQ.algebraic_field(*K_gens) if K_gens else QQ
        poly_K = minpoly(alpha, x_dummy, domain=K_domain)
        deg_K = degree(poly_K, x_dummy)
        h1_ok = bool(deg_K > 0)
    except Exception:
        h1_ok = False
        
    # neg_Q: degree of minpoly of alpha over M is strictly greater than degree over K
    try:
        M_domain = QQ.algebraic_field(*M_gens) if M_gens else QQ
        poly_M = minpoly(alpha, x_dummy, domain=M_domain)
        deg_M = degree(poly_M, x_dummy)
        
        # Recompute deg_K just to be safe in this block
        K_domain = QQ.algebraic_field(*K_gens) if K_gens else QQ
        poly_K = minpoly(alpha, x_dummy, domain=K_domain)
        deg_K = degree(poly_K, x_dummy)
        
        neg_q_ok = bool(deg_M > deg_K)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: alpha is algebraic over K",
    "¬Q: degree of minimal polynomial of alpha over M is strictly greater than degree over K"
]

N_HYP = 1
NEG_Q_INDEX = 1