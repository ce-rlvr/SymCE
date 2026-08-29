import sympy
from sympy import Poly
from sympy.abc import x, y

ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness):
    try:
        R, f, g = witness
    except Exception:
        return [False, False, False]
    
    try:
        Poly(x, x, domain=R)
        h1 = True
    except Exception:
        h1 = False
        
    try:
        g_sym = sympy.sympify(g)
        if not g_sym.free_symbols.issubset({y}):
            h2 = False
        else:
            Poly(g_sym, y, domain=R)
            h2 = True
    except Exception:
        h2 = False
        
    try:
        f_sym = sympy.sympify(f)
        if not f_sym.free_symbols.issubset({x}):
            neg_q = True
        else:
            Poly(f_sym, x, domain=R)
            neg_q = False
    except Exception:
        neg_q = True
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: g is a polynomial in y over R",
    "¬Q: The tensor product is not isomorphic to the quotient"
]

N_HYP = 2
NEG_Q_INDEX = 2