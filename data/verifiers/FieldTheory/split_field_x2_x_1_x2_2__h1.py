import sympy
from sympy import factor_list, Poly, Symbol, sqrt

# Top-level setup
x = Symbol('x')

def is_valid_poly(f):
    try:
        if not hasattr(f, 'free_symbols'):
            return False
        if not f.free_symbols.issubset({x}):
            return False
        p = Poly(f, x)
        return all(c.is_Rational for c in p.coeffs()) and p.degree() >= 1
    except Exception:
        return False

def splits_over(f, ext):
    try:
        coef, factors = factor_list(f, extension=ext)
        for fac, mult in factors:
            if Poly(fac, x).degree() > 1:
                return False
        return True
    except Exception:
        return False

def conditions(witness):
    f = witness
    
    h1 = is_valid_poly(f)
    
    try:
        if not h1:
            q = False
        else:
            splits_L = splits_over(f, sqrt(-3) + sqrt(2))
            if not splits_L:
                q = False
            else:
                splits_1 = splits_over(f, sqrt(-3))
                splits_2 = splits_over(f, sqrt(2))
                splits_3 = splits_over(f, sqrt(-6))
                
                if splits_1 or splits_2 or splits_3:
                    q = False
                else:
                    q = True
    except Exception:
        q = False

    neg_q = not q
    
    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = ["H_1: K is the splitting field of f(x) over Q", "¬Q: K is not Q(sqrt(-3) and sqrt(2)) or degree is not 4"]

N_HYP = 1
NEG_Q_INDEX = 1