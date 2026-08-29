import sympy
from sympy import Poly
from sympy.abc import x, y, z

def conditions(witness):
    try:
        f_expr, a_expr = witness
        
        f = Poly(f_expr, x)
        R = f.domain
        
        h1 = bool(R.is_UFD)
        h2 = not f.is_zero
        
        a = Poly(a_expr, x, domain=R)
        af = f * a
        
        c_af_val = af.content()
        c_f_val = f.content()
        
        rhs_expr = a_expr * c_f_val
        rhs_poly = Poly(rhs_expr, x, domain=R)
        
        if rhs_poly.degree() > 0:
            associated = False
        else:
            val_c_af = R.from_sympy(sympy.sympify(c_af_val))
            val_rhs = R.from_sympy(sympy.sympify(rhs_poly.eval(0)))
            
            if val_rhs == R.zero:
                associated = (val_c_af == R.zero)
            elif val_c_af == R.zero:
                associated = False
            else:
                q1, r1 = R.div(val_c_af, val_rhs)
                q2, r2 = R.div(val_rhs, val_c_af)
                associated = (r1 == R.zero and r2 == R.zero)
                
        neg_q = not associated
        
    except Exception:
        return [False, False, False]
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: f is a non-zero polynomial in R",
    "not Q: c(af) is not associated to a c(f) in R"
]

N_HYP = 2
NEG_Q_INDEX = 2