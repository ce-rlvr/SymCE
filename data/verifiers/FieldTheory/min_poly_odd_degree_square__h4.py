import sympy
from sympy import minpoly, Symbol, I, sqrt, Rational, degree, Expr, sympify

# Top-level setup
x = Symbol('x')

def conditions(witness) -> list[bool]:
    # Extract alpha from witness. We assume F = QQ and K = QQ(alpha).
    if isinstance(witness, tuple):
        alpha = witness[-1]
    else:
        alpha = witness

    # H_1: F is a field (QQ is a field)
    h1 = True
    
    # H_2: K is a field extension of F (QQ(alpha) is a field extension of QQ)
    h2 = True
    
    # H_3: alpha is an algebraic element over F
    try:
        alpha = sympify(alpha)
        if not isinstance(alpha, Expr):
            h3 = False
        else:
            p_alpha = minpoly(alpha, x)
            h3 = p_alpha is not None and degree(p_alpha, x) > 0
    except Exception:
        h3 = False

    # ¬Q: F(alpha) != F(alpha^2) or deg(minpoly(alpha^2)) != deg(minpoly(alpha))
    try:
        p_alpha2 = minpoly(alpha**2, x)
        deg_alpha = degree(p_alpha, x)
        deg_alpha2 = degree(p_alpha2, x)
        
        # Since F(alpha^2) is a subfield of F(alpha), F(alpha) == F(alpha^2) 
        # if and only if their degrees over F are equal.
        # Thus, the conclusion holds iff deg_alpha == deg_alpha2.
        conclusion = (deg_alpha == deg_alpha2)
        neg_q = not conclusion
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: K is a field extension of F",
    "H_3: alpha is an algebraic element over F",
    "¬Q: F(alpha) != F(alpha^2) or the minimal polynomial of alpha^2 over F has a different degree than that of alpha"
]

N_HYP = 3
NEG_Q_INDEX = 3