import sympy
from sympy.abc import x

def conditions(witness):
    try:
        m, n = witness
    except Exception:
        return [False, False]
    
    try:
        h1 = isinstance(m, (int, sympy.Integer)) and isinstance(n, (int, sympy.Integer)) and m > n and n > 0
    except Exception:
        h1 = False
        
    try:
        if not h1:
            neg_q = False
        else:
            poly_m = sympy.cyclotomic_poly(int(m), x)
            poly_n = sympy.cyclotomic_poly(int(n), x)
            res = sympy.resultant(poly_m, poly_n, x)
            neg_q = bool(res != 1)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: m and n are integers such that m > n > 0",
    "¬Q: The resultant of Phi_m(x) and Phi_n(x) is not exactly 1"
]

N_HYP = 1
NEG_Q_INDEX = 1