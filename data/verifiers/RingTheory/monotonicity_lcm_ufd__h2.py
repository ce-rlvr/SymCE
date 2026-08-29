import sympy
from sympy import lcm, div, cancel, fraction, Poly, ZZ, QQ
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: a divides b",
    "¬Q: lcm(a, c) does not divide lcm(b, c)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def get_lcm(u, v):
    try:
        if hasattr(u, 'lcm'):
            return u.lcm(v)
    except Exception:
        pass
    return lcm(u, v)

def divides(u, v):
    if hasattr(u, 'divides'):
        try:
            return u.divides(v)
        except Exception:
            pass
            
    try:
        if u == 0:
            return v == 0
    except Exception:
        pass
    
    try:
        if hasattr(u, 'is_integer') and hasattr(v, 'is_integer') and u.is_integer and v.is_integer:
            return v % u == 0
    except Exception:
        pass

    try:
        if isinstance(u, int) and isinstance(v, int):
            return v % u == 0
    except Exception:
        pass

    try:
        q, r = div(v, u)
        if r == 0:
            return True
    except Exception:
        pass
        
    try:
        ratio = cancel(v / u)
        num, den = fraction(ratio)
        if den in (1, -1):
            return True
    except Exception:
        pass
        
    return False

def conditions(witness):
    if isinstance(witness, (tuple, list)):
        if len(witness) == 4:
            R, a, b, c = witness
            try:
                h1 = bool(R.is_UFD)
            except Exception:
                h1 = True
        elif len(witness) == 3:
            a, b, c = witness
            h1 = True
        else:
            return [False, False, False]
    else:
        return [False, False, False]
        
    try:
        h2 = bool(divides(a, b))
    except Exception:
        h2 = False
        
    try:
        lcm_ac = get_lcm(a, c)
        lcm_bc = get_lcm(b, c)
        neg_q = not bool(divides(lcm_ac, lcm_bc))
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]