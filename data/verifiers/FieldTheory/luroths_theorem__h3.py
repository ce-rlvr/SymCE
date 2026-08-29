import sympy
from sympy.abc import x, y, z

# Top-level setup
QQ = sympy.QQ
ZZ = sympy.ZZ
RR = sympy.RR
CC = sympy.CC

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: x is transcendental over F",
    "¬Q: There does not exist u in K such that K = F(u)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        F, x_val, K = witness
    except Exception:
        return [False, False, False]
        
    # H_1: F is a field
    try:
        h1 = getattr(F, 'is_Field', False)
    except Exception:
        h1 = False
        
    # H_2: x is transcendental over F
    try:
        h2 = isinstance(x_val, sympy.Symbol)
        # Ensure x is not already one of the base generators of F (if F is a generated field/ring)
        if hasattr(F, 'symbols') and x_val in F.symbols:
            h2 = False
        if hasattr(F, 'domain') and hasattr(F.domain, 'symbols') and x_val in F.domain.symbols:
            h2 = False
    except Exception:
        h2 = False
        
    # ¬Q: K is NOT of the form F(u)
    try:
        neg_q = False
        if getattr(K, 'is_Field', False):
            # If K is a fraction field over F, it is F(u) iff it has exactly 1 generator.
            # If it has > 1 generators, its transcendence degree is > 1, so it cannot be F(u).
            if type(K).__name__ == 'FractionField' and K.domain == F:
                if len(K.symbols) > 1:
                    neg_q = True
            # Uncountable fields over QQ have infinite transcendence degree
            elif K in (sympy.CC, sympy.RR) and F == sympy.QQ:
                neg_q = True
        else:
            # If K is not a field, it cannot be F(u) since F(u) is a field.
            neg_q = True
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]