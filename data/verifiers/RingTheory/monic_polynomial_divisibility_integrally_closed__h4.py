import sympy
from sympy import Poly, ZZ, QQ
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: R is an integrally closed integral domain",
    "H_2: K is the field of fractions of R",
    "H_3: f and g are monic polynomials",
    "¬Q: f does not divide g"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    h1 = False
    h2 = False
    h3 = False
    neg_q = False
    
    try:
        if isinstance(witness, (tuple, list)) and len(witness) >= 2:
            f_val = witness[-2]
            g_val = witness[-1]
        else:
            return [False, False, False, False]
            
        f_expr = sympy.sympify(f_val)
        g_expr = sympy.sympify(g_val)
        
        gens = f_expr.free_symbols | g_expr.free_symbols
        if not gens:
            gen = x
        else:
            gen = sorted(list(gens), key=lambda s: s.name)[0]
            
        try:
            f_poly = Poly(f_expr, gen)
            g_poly = Poly(g_expr, gen)
        except Exception:
            return [False, False, False, False]
            
        if f_poly.domain in (ZZ, QQ) and g_poly.domain in (ZZ, QQ):
            h1 = True
            h2 = True
            
        if getattr(f_poly, 'is_monic', False) and getattr(g_poly, 'is_monic', False):
            h3 = True
            
        rem = sympy.rem(g_expr, f_expr, gen)
        if rem != 0:
            neg_q = True
            
    except Exception:
        pass
        
    return [h1, h2, h3, neg_q]