import sympy
from sympy import Poly
from sympy.abc import x

QQ = sympy.QQ
ZZ = sympy.ZZ
GF = sympy.GF

def conditions(witness):
    try:
        F, p = witness
    except Exception:
        return [False, False]
        
    try:
        h1 = bool(getattr(F, 'is_Field', False))
    except Exception:
        h1 = False
        
    try:
        p_poly = Poly(p, x, domain=F)
        if p_poly.is_zero:
            # F(x)/(0) is isomorphic to F(x), which is an integral domain but not a field.
            is_id = True
            is_field = False
        elif p_poly.degree() <= 0:
            # F(x)/(c) where c != 0 is the zero ring, which is neither an integral domain nor a field.
            is_id = False
            is_field = False
        else:
            # For a field F and deg(p) > 0, F(x)/(p) is an integral domain iff p is irreducible.
            # It is a field iff p is irreducible.
            is_irred = p_poly.is_irreducible
            is_id = is_irred
            is_field = is_irred
            
        iff_holds = (is_id == is_field)
        neg_q = not iff_holds
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = ["H_1: F is a field", "¬Q: The factor ring is an integral domain but not a field"]
N_HYP = 1
NEG_Q_INDEX = 1