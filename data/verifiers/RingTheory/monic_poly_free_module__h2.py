import sympy
from sympy import ZZ, QQ, RR, CC, S, Poly
from sympy.abc import x, y, z

def in_R(elem, R):
    if hasattr(R, '__contains__'):
        return elem in R
    if callable(R):
        return R(elem)
    return True

def conditions(witness):
    try:
        R, f = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: R is a commutative ring
    h1 = False
    try:
        if hasattr(R, 'is_commutative') and R.is_commutative:
            h1 = True
        elif isinstance(R, (list, set, tuple)):
            h1 = True
        elif R in [ZZ, QQ, RR, CC, S.Integers, S.Rationals, S.Reals, S.Complexes]:
            h1 = True
        elif hasattr(R, 'is_Ring') and R.is_Ring:
            h1 = True
        else:
            h1 = True
    except Exception:
        h1 = False
        
    # H2: f(x) is monic
    h2 = False
    try:
        p = Poly(f, x)
        if p.LC() == 1:
            h2 = True
    except Exception:
        h2 = False
        
    # H3: The degree of f(x) is n >= 1
    h3 = False
    try:
        p = Poly(f, x)
        if p.degree() >= 1:
            h3 = True
    except Exception:
        h3 = False
        
    # neg_Q: The factor ring R[x]/<f(x)> is not a free R-module of rank n
    neg_q = False
    try:
        p = Poly(f, x)
        has_one = False
        try:
            has_one = in_R(1, R)
        except Exception:
            has_one = True
            
        f_in_R = True
        try:
            for c in p.coeffs():
                if not in_R(c, R):
                    f_in_R = False
                    break
        except Exception:
            pass
            
        if not has_one or not f_in_R:
            neg_q = True
        else:
            neg_q = False
    except Exception:
        neg_q = True
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = ["H_1: R is a commutative ring", "H_2: f(x) is monic", "H_3: The degree of f(x) is n >= 1", "¬Q: The factor ring is not a free R-module of rank n"]

N_HYP = 3
NEG_Q_INDEX = 3