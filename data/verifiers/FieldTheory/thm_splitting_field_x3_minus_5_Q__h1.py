import sympy
from sympy import Symbol, Poly, root, sqrt, factor_list

x = Symbol('x')

def is_poly_in_Q(f):
    try:
        p = Poly(f, x)
        if p.is_zero:
            return False
        return all(c.is_Rational for c in p.coeffs())
    except Exception:
        return False

def splits_completely(f, ext):
    try:
        p = Poly(f, x)
        if p.degree() <= 1:
            return True
        _, fac_list = factor_list(f, extension=ext)
        for fac, mult in fac_list:
            if Poly(fac, x).degree() > 1:
                return False
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        H_1 = is_poly_in_Q(witness)
    except Exception:
        H_1 = False
    
    try:
        ext_K0 = [root(5, 3), sqrt(-3)]
        ext_Q_sqrt3 = [sqrt(-3)]
        
        splits_in_K0 = splits_completely(witness, ext_K0)
        splits_in_Q_sqrt3 = splits_completely(witness, ext_Q_sqrt3)
        
        conclusion_holds = splits_in_K0 and not splits_in_Q_sqrt3
        neg_Q = not conclusion_holds
    except Exception:
        neg_Q = False
        
    return [H_1, neg_Q]

CONDITION_LABELS = [
    "H_1: f(x) is a non-zero polynomial over Q",
    "¬Q: The splitting field of f(x) over Q is not Q(5**(1/3), sqrt(-3))"
]

N_HYP = 1
NEG_Q_INDEX = 1