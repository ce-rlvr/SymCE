import math
from sympy import Poly, Symbol, sqrt, QQ, I
from sympy.abc import x, y, z

def get_degree(domain):
    if hasattr(domain, 'degree'):
        return domain.degree()
    return 1

def conditions(witness):
    try:
        F, f, E, b, c = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: F is a field
    try:
        h1 = bool(F.is_Field)
    except Exception:
        h1 = False
        
    # H2: The characteristic of F is not equal to 2
    try:
        h2 = bool(F.characteristic != 2)
    except Exception:
        h2 = False
        
    # H3: E is a splitting field of f(x) over F
    try:
        if isinstance(f, Poly):
            f_poly = Poly(f, domain=F)
        else:
            syms = f.free_symbols
            if syms:
                f_poly = Poly(f, list(syms)[0], domain=F)
            else:
                f_poly = Poly(f, x, domain=F)
                
        f_E = Poly(f_poly, domain=E)
        factors = f_E.factor_list()[1]
        splits = all(fac.degree() == 1 for fac, mult in factors)
        
        f_F = Poly(f_poly, domain=F)
        splits_in_F = all(fac.degree() == 1 for fac, mult in f_F.factor_list()[1])
        
        deg_E = get_degree(E)
        
        if splits_in_F:
            h3 = bool(splits and deg_E == 1)
        else:
            h3 = bool(splits and 1 < deg_E <= math.factorial(f_poly.degree()))
    except Exception:
        h3 = False
        
    # ¬Q: E is not isomorphic to F(\sqrt{b^2 - 4c}) over F
    try:
        val = b**2 - 4*c
        sqrt_val = sqrt(val)
        
        try:
            F.from_expr(sqrt_val)
            deg_F_sqrt = 1
        except Exception:
            deg_F_sqrt = 2
            
        deg_E = get_degree(E)
        if deg_E != deg_F_sqrt:
            is_isomorphic = False
        else:
            try:
                E.from_expr(sqrt_val)
                is_isomorphic = True
            except Exception:
                is_isomorphic = False
                
        neg_q = not is_isomorphic
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: The characteristic of F is not equal to 2",
    "H_3: E is a splitting field of f(x) over F",
    "¬Q: E is not isomorphic to F(\\sqrt{b^2 - 4c}) over F"
]

N_HYP = 3
NEG_Q_INDEX = 3