import sympy
from sympy import symbols

QQ = sympy.QQ
ZZ = sympy.ZZ
FF = sympy.FF
CC = sympy.CC
RR = sympy.RR

def conditions(witness):
    try:
        domain, coeffs = witness
    except Exception:
        return [False, False, False, False]
    
    try:
        h1 = bool(domain.is_Field)
    except Exception:
        h1 = False
        
    try:
        h2 = bool(domain.characteristic != 2)
    except Exception:
        h2 = False
        
    try:
        h3 = True
        if len(coeffs) == 0:
            h3 = False
        for a in coeffs:
            if domain(a) == domain.zero:
                h3 = False
                break
    except Exception:
        h3 = False
        
    try:
        n = len(coeffs)
        if n == 0:
            neg_q = False
        else:
            xs = [symbols(f'x{i+1}') for i in range(n)]
            poly_expr = sum(domain.to_sympy(domain(a)) * x**2 for a, x in zip(coeffs, xs))
            coeff, factors = sympy.factor_list(poly_expr, domain=domain)
            total_mult = sum(mult for f, mult in factors)
            neg_q = bool(total_mult > 1)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: The characteristic of K is not 2",
    "H_3: a_i are non-zero elements of K",
    "¬Q: The polynomial sum a_i x_i^2 is reducible"
]

N_HYP = 3
NEG_Q_INDEX = 3