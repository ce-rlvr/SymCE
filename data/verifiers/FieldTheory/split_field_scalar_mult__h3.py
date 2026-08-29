import sympy
from sympy import Poly, QQ, ZZ, RR, CC
from sympy.abc import x

def conditions(witness):
    try:
        F, f, K, c = witness
    except Exception:
        return [False, False, False, False]
    
    try:
        h1 = bool(F.is_Field)
    except Exception:
        h1 = False
        
    try:
        if isinstance(f, Poly):
            h2 = (f.domain == F)
        else:
            f_poly = Poly(f, x, domain=F)
            h2 = (f_poly.domain == F)
    except Exception:
        h2 = False
        
    try:
        if isinstance(f, Poly):
            poly_f = f
        else:
            poly_f = Poly(f, x, domain=F)
            
        if poly_f.is_zero:
            h3 = False
        else:
            roots = poly_f.all_roots()
            expected_K = F.algebraic_field(*roots)
            h3 = (K == expected_K)
    except Exception:
        h3 = False
        
    try:
        if isinstance(f, Poly):
            poly_f = f
        else:
            poly_f = Poly(f, x, domain=F)
            
        cf = poly_f * c
        if cf.is_zero:
            is_split = False
        else:
            roots_cf = cf.all_roots()
            expected_K_cf = F.algebraic_field(*roots_cf)
            is_split = (K == expected_K_cf)
        neg_q = not is_split
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = ['H_1: F is a field', 'H_2: f is a polynomial over F', 'H_3: K is the splitting field of f over F', 'neg_Q: K is not the splitting field of c f over F']

N_HYP = 3
NEG_Q_INDEX = 3