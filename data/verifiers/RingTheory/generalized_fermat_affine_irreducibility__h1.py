import sympy
from sympy import factor_list
from sympy.abc import x, y
from sympy.polys.domains import QQ, ZZ, FF, GF

def conditions(witness):
    try:
        n, K = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = bool(int(n) == n and n >= 1)
    except Exception:
        h1 = False
        
    try:
        char = K.characteristic
        if char == 0:
            h2 = True
        else:
            h2 = bool(n % char != 0)
    except Exception:
        h2 = False
        
    try:
        poly = x**n + y**n + 1
        coeff, factors = factor_list(poly, x, y, domain=K)
        deg_sum = sum(mult for f, mult in factors)
        neg_q = bool(deg_sum > 1)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n >= 1 is an integer",
    "H_2: The characteristic of K does not divide n",
    "¬Q: The polynomial x^n + y^n + 1 is reducible"
]

N_HYP = 2
NEG_Q_INDEX = 2