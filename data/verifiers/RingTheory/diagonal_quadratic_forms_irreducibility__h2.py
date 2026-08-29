import sympy
from sympy import symbols, Poly
from sympy.polys.domains import GF, QQ, ZZ, RR, CC

# Top-level setup
# The witness is expected to be a tuple: (K, a_list)
# where K is a SymPy domain (e.g., GF(2)) and a_list is a list of coefficients.

def conditions(witness):
    try:
        K, a_list = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: K is a field
    try:
        h1 = bool(getattr(K, 'is_Field', False))
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
            val = K(a)
            if val == K.zero:
                h3 = False
                break
    except Exception:
        h3 = False
        
    # neg_Q: The polynomial sum(a_i x_i^2) is reducible over K
    try:
        x = symbols(f'x1:{n+1}')
        expr = sum(K.to_sympy(K(a)) * x[i]**2 for i, a in enumerate(a_list))
        p = Poly(expr, *x, domain=K)
        
        try:
            factors = p.factor_list()
            neg_q = (len(factors[1]) > 1) or (len(factors[1]) == 1 and factors[1][0][1] > 1)
        except Exception:
            irr = p.is_irreducible
            if irr is not None:
                neg_q = not irr
            else:
                neg_q = (getattr(K, 'characteristic', None) == 2)
    except Exception:
        try:
            neg_q = (getattr(K, 'characteristic', None) == 2)
        except Exception:
            neg_q = False
            
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: n >= 3 is an integer",
    "H_3: a_1, ..., a_n are non-zero elements of K",
    "¬Q: The polynomial sum(a_i x_i^2) is reducible over K"
]

N_HYP = 3
NEG_Q_INDEX = 3