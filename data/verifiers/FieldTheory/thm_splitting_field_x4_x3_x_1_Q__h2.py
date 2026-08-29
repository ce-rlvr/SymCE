import sympy
from sympy import Symbol, simplify, sympify

x = Symbol('x')

def conditions(witness):
    try:
        expr = sympify(witness)
        h1 = bool(simplify(expr - (x**4 + x**3 + x + 1)) == 0)
    except Exception:
        h1 = False

    try:
        expr = sympify(witness)
        expr = sympy.cancel(expr)
        
        if expr == 0 or sympy.degree(expr, x) < 1:
            concl = False
        else:
            factors = sympy.factor_list(expr, domain='QQ')
            has_deg_2 = False
            concl = True
            
            for fac, mult in factors[1]:
                deg = sympy.degree(fac, x)
                if deg == 1:
                    continue
                elif deg == 2:
                    has_deg_2 = True
                    a = fac.coeff(x, 2)
                    b = fac.coeff(x, 1)
                    c = fac.coeff(x, 0)
                    disc = b**2 - 4*a*c
                    
                    val = simplify(disc / sympy.Integer(-3))
                    if val <= 0:
                        concl = False
                        break
                    if not sympy.sqrt(val).is_rational:
                        concl = False
                        break
                else:
                    concl = False
                    break
            
            if not has_deg_2:
                concl = False
                
        neg_q = not concl
    except Exception:
        neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f(x) = x^4 + x^3 + x + 1 over Q",
    "¬Q: The splitting field K is not Q(sqrt(-3)) or the degree of K over Q is not 2"
]
N_HYP = 1
NEG_Q_INDEX = 1