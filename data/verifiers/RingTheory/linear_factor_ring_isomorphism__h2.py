import sympy
from sympy import Symbol, S

x = Symbol('x')
ZZ = S.Integers

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, a = witness
        else:
            R = ZZ
            a = witness
            
        if hasattr(R, 'is_commutative'):
            h1 = bool(R.is_commutative)
        elif R == ZZ:
            h1 = True
        else:
            h1 = True
            
        a_expr = sympy.sympify(a)
        poly = sympy.poly(x - a_expr, x)
        
        if poly is None:
            neg_q = True
        else:
            deg = poly.degree()
            if deg != 1:
                neg_q = True
            else:
                lc = poly.coeffs()[0]
                if R == ZZ:
                    if lc in [1, -1]:
                        neg_q = False
                    else:
                        neg_q = True
                else:
                    try:
                        if lc in [1, -1]:
                            neg_q = False
                        else:
                            inv = 1 / lc
                            if hasattr(R, '__contains__') and inv in R:
                                neg_q = False
                            else:
                                neg_q = True
                    except Exception:
                        neg_q = True
                        
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "¬Q: The factor ring of polynomials over R modulo x - a is not isomorphic to R"
]

N_HYP = 1
NEG_Q_INDEX = 1