import sympy
from sympy import QQ, ZZ, Symbol
import math

x = Symbol('x')

def conditions(witness):
    try:
        F, f, K = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = F.is_Field
    except Exception:
        h1 = False
        
    n = 1
    try:
        if isinstance(f, sympy.Poly):
            n = f.degree()
            h2 = (n >= 1) and (f.domain == F)
        else:
            poly_f = sympy.Poly(f, x, domain=F)
            n = poly_f.degree()
            h2 = (n >= 1)
    except Exception:
        h2 = False
        
    try:
        try:
            deg_K = int(K)
        except (TypeError, ValueError, AttributeError):
            if callable(getattr(K, 'degree', None)):
                deg_K = int(K.degree())
            else:
                deg_K = int(K.degree)
                
        neg_q = (math.factorial(n) % deg_K != 0)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f(x) is a polynomial over F of degree n >= 1",
    "¬Q: The degree of the field extension K over F does not divide n!"
]

N_HYP = 2
NEG_Q_INDEX = 2