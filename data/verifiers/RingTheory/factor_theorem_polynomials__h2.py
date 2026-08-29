import sympy
from sympy import Poly, simplify, sympify
from sympy.abc import x

QQ = sympy.QQ
RR = sympy.RR
CC = sympy.CC
ZZ = sympy.ZZ

def conditions(witness):
    try:
        F, a, f = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = bool(F.is_Field)
    except Exception:
        h1 = False
        
    try:
        h2 = bool(a in F)
    except Exception:
        h2 = False
        
    try:
        f_expr = sympify(f)
        
        try:
            poly_f = Poly(f_expr, x, domain=F)
            poly_xa = Poly(x - a, x, domain=F)
            q, r = poly_f.div(poly_xa)
            divides = bool(r.is_zero)
        except Exception:
            divides = False
            
        try:
            val = f_expr.subs(x, a)
            f_a_zero = bool(simplify(val) == 0)
        except Exception:
            f_a_zero = False
            
        neg_q = bool(divides != f_a_zero)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: a is an element of F",
    "not Q: x - a divides f in polynomial ring iff f(a) = 0 fails"
]

N_HYP = 2
NEG_Q_INDEX = 2