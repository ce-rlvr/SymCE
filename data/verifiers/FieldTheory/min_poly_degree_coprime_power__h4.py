import sympy
from sympy import minpoly, degree, Symbol, sqrt, I, Rational
from sympy.polys.domains import QQ, ZZ, RR, CC, GF

x = Symbol('x')

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: α is algebraic over F",
    "H_3: The minimal polynomial of α over F has degree n",
    "¬Q: The minimal polynomial of α^k over F does not have degree n"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        F, alpha, n, k = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: F is a field
    try:
        h1 = bool(F.is_Field)
    except Exception:
        h1 = False
        
    # H2: α is algebraic over F
    try:
        p_alpha = minpoly(alpha, x, domain=F)
        h2 = True
    except Exception:
        h2 = False
        
    # H3: The minimal polynomial of α over F has degree n
    try:
        p_alpha = minpoly(alpha, x, domain=F)
        h3 = bool(degree(p_alpha, x) == n)
    except Exception:
        h3 = False
        
    # ¬Q: The minimal polynomial of α^k over F does not have degree n
    try:
        p_alphak = minpoly(alpha**k, x, domain=F)
        neg_q = bool(degree(p_alphak, x) != n)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]