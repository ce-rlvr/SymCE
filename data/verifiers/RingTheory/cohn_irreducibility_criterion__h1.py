import sympy
from sympy import isprime, Poly
from sympy.abc import x

def conditions(witness):
    try:
        b, f = witness
    except Exception:
        return [False, False, False, False]
    
    try:
        h1 = isinstance(b, int) and b >= 2
    except Exception:
        h1 = False
        
    try:
        poly_f = Poly(f, x)
        coeffs = poly_f.all_coeffs()
        h2 = all(0 <= c < b for c in coeffs)
    except Exception:
        h2 = False
        
    try:
        val = int(f.subs(x, b))
        h3 = isprime(val)
    except Exception:
        h3 = False
        
    try:
        poly_f_Z = Poly(f, x, domain='ZZ')
        c, factors = sympy.factor_list(poly_f_Z)
        if c == 0:
            neg_q = True
        else:
            c_factors = sympy.factorint(abs(c))
            num_c_factors = sum(c_factors.values())
            num_poly_factors = sum(mult for _, mult in factors)
            total_factors = num_c_factors + num_poly_factors
            neg_q = total_factors != 1
    except Exception:
        neg_q = True
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = ["H_1: b >= 2 is an integer", "H_2: The coefficients satisfy 0 <= a_i < b", "H_3: The integer evaluated value f(b) is a prime number", "neg_Q: f(x) is reducible over Z"]

N_HYP = 3
NEG_Q_INDEX = 3