import math
from sympy import Poly, GF
from sympy.abc import x

def _lcm(a, b):
    return abs(a * b) // math.gcd(a, b) if a and b else 0

def conditions(witness):
    # H_1: F_2 is the finite field with 2 elements
    h1 = True
    
    # H_2: f(x) is a polynomial over F_2
    try:
        f_poly = Poly(witness, x, domain=GF(2))
        h2 = True
    except Exception:
        h2 = False
        
    # neg_Q: The degree of the splitting field of f(x) over F_2 is not 4
    try:
        if not h2:
            neg_q = False
        else:
            if f_poly.is_zero:
                deg = 1
            else:
                factors = f_poly.factor_list()
                deg = 1
                for factor, mult in factors[1]:
                    deg = _lcm(deg, factor.degree())
            neg_q = bool(deg != 4)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F_2 is the finite field with 2 elements",
    "H_2: f(x) is a polynomial over F_2",
    "¬Q: The degree of the splitting field of f(x) over F_2 is not 4"
]

N_HYP = 2
NEG_Q_INDEX = 2