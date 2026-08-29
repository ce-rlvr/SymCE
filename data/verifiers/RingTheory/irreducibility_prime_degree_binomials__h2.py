import sympy
from sympy import Symbol, Poly, QQ, ZZ, GF, Rational
from sympy.abc import x

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: a is an element of F",
    "H_3: There does not exist any element c in F such that c^p = a",
    "¬Q: The polynomial x^p - a is not irreducible over F"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        F, a, p = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: F is a field
    try:
        h1 = getattr(F, 'is_Field', False)
    except Exception:
        h1 = False
        
    # H_2: a is an element of F
    try:
        h2 = a in F
    except Exception:
        h2 = False
        
    # H_3: There does not exist any element c in F such that c^p = a
    try:
        p_val = int(p)
        if p_val == p and p_val > 0:
            poly = Poly(x**p_val - a, x, domain=F)
            roots = poly.ground_roots()
            h3 = len(roots) == 0
        else:
            h3 = False
    except Exception:
        h3 = False
        
    # ¬Q: The polynomial x^p - a is not irreducible over F
    try:
        p_val = int(p)
        if p_val == p and p_val > 0:
            poly = Poly(x**p_val - a, x, domain=F)
            neg_q = not poly.is_irreducible
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]