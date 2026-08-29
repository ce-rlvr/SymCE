import sympy
from sympy.abc import x

def conditions(witness):
    try:
        n = int(witness)
        if n < 0:
            return [False]
        
        expr = x**n - x - 1
        p = sympy.Poly(expr, x, domain='QQ')
        
        # A polynomial is irreducible if it has degree >= 1 and cannot be factored.
        # Units (degree < 1) are not irreducible.
        if p.degree() < 1:
            neg_q = True
        else:
            neg_q = not sympy.is_irreducible(expr, domain='QQ')
            
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The polynomial x^n - x - 1 is not irreducible over Q"
]

N_HYP = 0
NEG_Q_INDEX = 0