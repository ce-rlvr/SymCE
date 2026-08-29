import sympy
from sympy import symbols, factor_list, QQ, ZZ, GF

x, y = symbols('x y')

def conditions(witness):
    try:
        K, n = witness
    except Exception:
        return [False, False, False]
    
    # H1: K is a field
    try:
        h1 = bool(K.is_Field)
    except Exception:
        h1 = False
        
    # H2: The characteristic of K does not divide n
    try:
        char = getattr(K, 'char', getattr(K, 'characteristic', 0))
        if char == 0:
            h2 = True
        else:
            h2 = bool(n % char != 0)
    except Exception:
        h2 = False
        
    # neg_Q: x^n + y^n + 1 is not irreducible
    try:
        if not isinstance(n, int) or n < 1:
            neg_q = False
        else:
            poly = x**n + y**n + 1
            coeff, factors = factor_list(poly, domain=K)
            
            # A polynomial is irreducible if it has exactly one non-constant factor with multiplicity 1
            if len(factors) != 1 or factors[0][1] > 1:
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: The characteristic of K does not divide n",
    "neg_Q: The polynomial x^n + y^n + 1 is not irreducible"
]

N_HYP = 2
NEG_Q_INDEX = 2