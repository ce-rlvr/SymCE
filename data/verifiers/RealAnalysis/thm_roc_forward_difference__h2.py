import sympy
from sympy import abc

x = sympy.Symbol('x')

def conditions(witness):
    try:
        A_x = witness
        num, den = sympy.cancel(A_x).as_numer_denom()
        
        if den.subs(x, 0) == 0:
            return [False, False]
        
        poles_A = sympy.roots(den, x)
        if not poles_A and sympy.degree(den, x) > 0:
            return [False, False]
        
        if poles_A:
            R = min([float(abs(p.evalf())) for p in poles_A])
        else:
            R = float('inf')
            
        h1_ok = True
        
        D_x = sympy.cancel((1 / (1 + x)) * A_x.subs(x, x / (1 + x)))
        num_D, den_D = D_x.as_numer_denom()
        
        poles_D = sympy.roots(den_D, x)
        if not poles_D and sympy.degree(den_D, x) > 0:
            return [True, False]
            
        if poles_D:
            R_D = min([float(abs(p.evalf())) for p in poles_D])
        else:
            R_D = float('inf')
            
        min_R_1 = min(R, 1.0)
        neg_q = R_D < min_R_1
        
        return [h1_ok, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: sum a_n x^n is a power series with radius of convergence R",
    "¬Q: The radius of convergence of sum d_n x^n is strictly less than min(R, 1)"
]

N_HYP = 1
NEG_Q_INDEX = 1