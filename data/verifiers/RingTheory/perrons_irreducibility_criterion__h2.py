import sympy
from sympy import Poly, Symbol

x = Symbol('x')

def conditions(witness) -> list[bool]:
    try:
        f = Poly(witness, x)
        n = f.degree()
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = bool(n >= 2)
    except Exception:
        h1 = False
        
    try:
        coeffs = f.all_coeffs()
        a_0 = coeffs[-1]
        h2 = bool(a_0 != 0)
    except Exception:
        h2 = False
        
    try:
        if n >= 2:
            a_n_minus_1 = coeffs[1]
            sum_abs = sum(abs(c) for c in coeffs[2:])
            h3 = bool(abs(a_n_minus_1) > 1 + sum_abs)
        else:
            h3 = False
    except Exception:
        h3 = False
        
    try:
        factors = sympy.factor_list(f, domain='QQ')
        num_factors = sum(mult for factor, mult in factors[1] if factor.degree() > 0)
        neg_q = bool(num_factors > 1)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer with n >= 2",
    "H_2: a_0 is not equal to 0",
    "H_3: |a_{n-1}| > 1 + |a_{n-2}| + ... + |a_0|",
    "¬Q: f(x) is reducible over the rational numbers Q"
]

N_HYP = 3
NEG_Q_INDEX = 3