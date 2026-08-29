import sympy
import math

def conditions(witness):
    try:
        if len(witness) != 3:
            return [False, False]
        x, y, p = witness
    except Exception:
        return [False, False]
        
    try:
        h1 = isinstance(x, (int, sympy.Integer)) and isinstance(y, (int, sympy.Integer))
    except Exception:
        h1 = False
        
    try:
        if not isinstance(p, (int, sympy.Integer)):
            neg_q = False
        else:
            x_i = int(x)
            y_i = int(y)
            p_i = int(p)
            
            lhs = pow(x_i + y_i, p_i, p_i)
            rhs = (pow(x_i, p_i, p_i) + pow(y_i, p_i, p_i)) % p_i
            neg_q = bool(lhs != rhs)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x and y are integers",
    "¬Q: (x+y)^p is not congruent to x^p + y^p (mod p)"
]

N_HYP = 1
NEG_Q_INDEX = 1