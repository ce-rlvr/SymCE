import sympy
from sympy import cyclotomic_poly, expand
from sympy.abc import x

def conditions(witness):
    try:
        n, p = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = (isinstance(n, int) or isinstance(n, sympy.Integer)) and n >= 1
    except Exception:
        h1 = False
        
    try:
        h2 = (isinstance(p, int) or isinstance(p, sympy.Integer)) and p != 0 and (n % p != 0)
    except Exception:
        h2 = False
        
    try:
        if not (h1 and (isinstance(p, int) or isinstance(p, sympy.Integer)) and p >= 1):
            neg_q = False
        else:
            n_int = int(n)
            p_int = int(p)
            
            lhs = cyclotomic_poly(p_int * n_int, x)
            num = cyclotomic_poly(n_int, x**p_int)
            den = cyclotomic_poly(n_int, x)
            
            # Check if Phi_{pn}(x) == Phi_n(x^p) / Phi_n(x)
            # Equivalently, check if Phi_{pn}(x) * Phi_n(x) == Phi_n(x^p)
            eq = expand(lhs * den) == expand(num)
            neg_q = not eq
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: n >= 1 is an integer",
    "H_2: p does not divide n",
    "¬Q: Phi_{pn}(x) != Phi_n(x^p) / Phi_n(x)"
]

N_HYP = 2
NEG_Q_INDEX = 2