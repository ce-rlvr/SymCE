import sympy
from sympy import symbols

QQ = sympy.QQ
ZZ = sympy.ZZ
RR = sympy.RR
CC = sympy.CC

x, y = symbols('x y')

def conditions(witness):
    try:
        F, n, m = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = hasattr(F, 'is_Field') and bool(F.is_Field)
    except Exception:
        h1 = False
        
    try:
        h2 = isinstance(n, (int, sympy.Integer)) and isinstance(m, (int, sympy.Integer)) and n > 0 and m > 0
    except Exception:
        h2 = False
        
    try:
        if not h2:
            neg_q = False
        else:
            poly = x**n - y**m
            factors = sympy.factor_list(poly, domain=F)
            num_factors = sum(exp for f, exp in factors[1])
            neg_q = num_factors > 1
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: n and m are positive integers",
    "not Q: x^n - y^m is reducible over F"
]

N_HYP = 2
NEG_Q_INDEX = 2