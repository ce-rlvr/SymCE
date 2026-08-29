import sympy
from sympy import Symbol, minpoly, factor_list, degree, QQ, ZZ, I, sqrt, Rational

# Top-level setup
x = Symbol('x')

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: alpha is algebraic over F",
    "¬Q: The minimal polynomial of alpha over F(t) is NOT equal to the minimal polynomial of alpha over F"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Given a witness tuple (F, alpha, t), checks if it is a valid counterexample.
    F: a SymPy field domain (e.g., QQ)
    alpha: an algebraic element over F
    t: an element (algebraic over F for a counterexample)
    """
    try:
        F, alpha, t = witness
    except Exception:
        return [False, False, False]
        
    # H_1: F is a field
    try:
        h1_ok = bool(getattr(F, 'is_Field', False) or getattr(F, 'is_field', False) or F == QQ)
    except Exception:
        h1_ok = False
        
    # H_2: alpha is algebraic over F
    try:
        poly_F = minpoly(alpha, x, domain=F)
        h2_ok = bool(poly_F.has(x) and degree(poly_F, x) >= 1)
    except Exception:
        h2_ok = False
        
    # ¬Q: The minimal polynomial of alpha over F(t) is NOT equal to the minimal polynomial of alpha over F
    try:
        if not h2_ok:
            neg_q_ok = False
        else:
            # If poly_F factors over F(t), then the minimal polynomial over F(t) 
            # is a proper divisor of poly_F, hence they are not equal.
            # If t is transcendental, extension=t will raise an exception, 
            # which correctly falls to False (since minpoly wouldn't change).
            coeff, factors = factor_list(poly_F, extension=t)
            
            # It factors non-trivially if there are multiple factors or a repeated factor
            if len(factors) > 1 or (len(factors) == 1 and factors[0][1] > 1):
                neg_q_ok = True
            else:
                neg_q_ok = False
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]