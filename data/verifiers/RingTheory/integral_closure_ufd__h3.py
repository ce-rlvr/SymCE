import sympy
from sympy import Poly
from sympy.abc import x
from sympy import ZZ, QQ

def conditions(witness):
    try:
        R, f, alpha = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = bool(getattr(R, 'is_UFD', False))
    except Exception:
        h1 = False
        
    try:
        if isinstance(f, Poly):
            f_poly = f
        else:
            f_poly = Poly(f, x)
            
        if len(f_poly.gens) > 1:
            h2 = False
        else:
            is_monic = (f_poly.LC() == 1)
            coeffs_in_R = all((c in R) for c in f_poly.coeffs())
            h2 = bool(is_monic and coeffs_in_R)
    except Exception:
        h2 = False
        
    try:
        neg_q = bool(alpha not in R)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = ['H_1: R is a UFD', 'H_2: f is a monic polynomial over R', '¬Q: alpha is not in R']
N_HYP = 2
NEG_Q_INDEX = 2