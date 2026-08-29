import sympy
from sympy import symbols
from sympy.polys.domains import QQ, ZZ, GF, RR, CC

x, y = symbols('x y')

def conditions(witness):
    try:
        K, n = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = bool(getattr(K, 'is_Field', False))
    except Exception:
        h1 = False
        
    try:
        h2 = isinstance(n, (int, sympy.Integer)) and int(n) >= 1
    except Exception:
        h2 = False
        
    try:
        poly = x**int(n) + y**int(n) + 1
        _, factors = sympy.factor_list(poly, x, y, domain=K)
        is_irred = (len(factors) == 1 and factors[0][1] == 1)
        neg_q = not is_irred
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: n >= 1 is an integer",
    "¬Q: x^n + y^n + 1 is not irreducible"
]

N_HYP = 2
NEG_Q_INDEX = 2