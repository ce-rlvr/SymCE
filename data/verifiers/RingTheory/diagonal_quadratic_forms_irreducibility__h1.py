import sympy
from sympy import ZZ, QQ, GF

def conditions(witness):
    try:
        K, a_list = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: The characteristic of K is not 2
    try:
        h1 = bool(K.characteristic != 2)
    except Exception:
        h1 = False
        
    # H_2: n >= 3 is an integer
    try:
        n = len(a_list)
        h2 = bool(n >= 3)
    except Exception:
        h2 = False
        
    # H_3: a_1, ..., a_n are non-zero elements of K
    try:
        h3 = True
        for a in a_list:
            if K(a) == K.zero:
                h3 = False
                break
    except Exception:
        h3 = False
        
    # neg_Q: The polynomial is reducible in K[x_1, ..., x_n]
    try:
        x = [sympy.Symbol('x{}'.format(i+1)) for i in range(n)]
        poly_expr = sum(a_list[i] * x[i]**2 for i in range(n))
        
        c, factors = sympy.factor_list(poly_expr, domain=K)
        
        is_irred = (len(factors) == 1 and factors[0][1] == 1)
        neg_q = not is_irred
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: The characteristic of K is not 2",
    "H_2: n >= 3 is an integer",
    "H_3: a_1, ..., a_n are non-zero elements of K",
    "¬Q: The polynomial is reducible"
]

N_HYP = 3
NEG_Q_INDEX = 3