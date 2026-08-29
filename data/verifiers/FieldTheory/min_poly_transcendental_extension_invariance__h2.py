import sympy
from sympy import QQ, ZZ

def conditions(witness):
    try:
        F, alpha, t = witness
    except Exception:
        return [False, False, False]
        
    # H1: F is a field
    try:
        h1 = bool(F.is_Field)
    except Exception:
        h1 = False
        
    # H2: t is an element transcendental over F(alpha)
    try:
        if isinstance(t, sympy.Symbol):
            if hasattr(F, 'gens') and t in F.gens:
                h2 = False
            elif hasattr(alpha, 'free_symbols') and t in alpha.free_symbols:
                h2 = False
            else:
                h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # neg_Q: The minimal polynomial of alpha over F(t) is NOT equal to the minimal polynomial of alpha over F
    try:
        x = sympy.Symbol('x')
        try:
            mp_F = sympy.minpoly(alpha, x, domain=F)
            # If minpoly succeeds, alpha is algebraic over F.
            # Since t is transcendental over F(alpha), alpha is also algebraic over F(t)
            # and the minimal polynomials are equal.
            neg_q = False
        except Exception as e:
            # If alpha is transcendental over F, it has no minimal polynomial over F.
            # Thus the statement "The minimal polynomial ... is equal to ..." is false.
            if type(e).__name__ == 'NotAlgebraic' or "not algebraic" in str(e).lower():
                neg_q = True
            elif (isinstance(alpha, sympy.Symbol) or getattr(alpha, 'is_transcendental', False)) and F in (sympy.QQ, sympy.ZZ):
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: t is an element transcendental over F(alpha)",
    "¬Q: The minimal polynomial of alpha over F(t) is not equal to the minimal polynomial of alpha over F"
]

N_HYP = 2
NEG_Q_INDEX = 2