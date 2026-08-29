import sympy
from sympy import ZZ, QQ, Poly, Rational
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: a is a non-zero element in R",
    "¬Q: The content c(af) is not associated to a * c(f) in R"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        R, a, f = witness
    except Exception:
        return [False, False, False]
        
    # H_1: R is a Unique Factorization Domain
    try:
        h1 = getattr(R, 'is_UFD', False)
    except Exception:
        h1 = False
        
    # H_2: a is a non-zero element in R
    try:
        h2 = (a in R) and (a != 0)
    except Exception:
        h2 = False
        
    # ¬Q: The content c(af) is not associated to a * c(f) in R
    try:
        if not isinstance(f, sympy.Poly):
            f = sympy.Poly(f)
            
        af = f * a
        
        c_f = f.content()
        c_af = af.content()
        
        a_cf = a * c_f
        
        def are_associated(u, v, R):
            if u not in R or v not in R:
                return False
            if u == 0 and v == 0:
                return True
            if u == 0 or v == 0:
                return False
            try:
                u_s = sympy.S(u)
                v_s = sympy.S(v)
                q1 = sympy.cancel(u_s / v_s)
                q2 = sympy.cancel(v_s / u_s)
                return (q1 in R) and (q2 in R)
            except Exception:
                return False
                
        Q = are_associated(c_af, a_cf, R)
        neg_Q = not Q
    except Exception:
        neg_Q = False
        
    return [bool(h1), bool(h2), bool(neg_Q)]