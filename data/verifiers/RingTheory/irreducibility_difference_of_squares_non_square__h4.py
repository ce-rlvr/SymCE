import sympy
from sympy import symbols, QQ, RR, CC, ZZ, GF

x, y = symbols('x y')

def conditions(witness) -> list[bool]:
    try:
        F, a = witness
    except Exception:
        return [False, False, False, False]
    
    try:
        h1 = bool(F.is_Field)
    except Exception:
        h1 = False
        
    try:
        h2 = bool(F.characteristic != 2)
    except Exception:
        h2 = False
        
    try:
        h3 = bool(F(a) != F(0))
    except Exception:
        h3 = False
        
    try:
        if hasattr(F, 'to_sympy'):
            a_sym = F.to_sympy(F(a))
        else:
            a_sym = sympy.sympify(a)
            
        poly = x**2 - a_sym * y**2
        coeff, factors = sympy.factor_list(poly, domain=F)
        total_mult = sum(mult for f, mult in factors)
        neg_q = bool(total_mult > 1)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: The characteristic of F is not equal to 2",
    "H_3: a in F is a non-zero element",
    "¬Q: The polynomial x^2 - a*y^2 is reducible"
]

N_HYP = 3
NEG_Q_INDEX = 3