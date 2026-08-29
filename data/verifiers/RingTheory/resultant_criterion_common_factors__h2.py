import sympy
from sympy import Poly, gcd, resultant
from sympy.abc import x

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
        f, g = witness
        f = sympy.sympify(f)
        g = sympy.sympify(g)
    except Exception:
        return [False, False]
        
    try:
        pf = Poly(f, x)
        pg = Poly(g, x)
        h1 = True
    except Exception:
        h1 = False
        
    try:
        if f == 0 and g == 0:
            has_common_factor = True
        else:
            has_common_factor = Poly(gcd(f, g), x).degree() > 0
            
        res_fg = resultant(f, g, x)
        res_is_zero = (res_fg == 0)
        
        iff_holds = (has_common_factor == res_is_zero)
        neg_q = not iff_holds
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = ["H_1: F is a field", "¬Q: The equivalence fails"]
N_HYP = 1
NEG_Q_INDEX = 1