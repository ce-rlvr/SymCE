import sympy as sp
from sympy.abc import x

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        n = None
        poly = None
        
        if isinstance(witness, int):
            n = witness
            if n > 0:
                poly = x**n - 2
        elif isinstance(witness, tuple):
            if len(witness) == 2:
                poly, n = witness
            elif len(witness) == 3:
                _, poly, n = witness
                
        if isinstance(n, int) and n > 0:
            h1 = True
            
        if h1 and isinstance(poly, sp.Expr):
            poly_obj = sp.Poly(poly, x, domain=sp.QQ)
            if poly_obj.degree() == n and poly_obj.is_irreducible:
                h2 = True
                
        if h1 and h2:
            if n == 1:
                neg_q = False
            else:
                ext = sp.RootOf(poly_obj, 0)
                for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]:
                    test_poly = x**n - p
                    test_poly_obj = sp.Poly(test_poly, x, domain=sp.QQ)
                    if test_poly_obj.is_irreducible and test_poly_obj != poly_obj:
                        factors = sp.factor_list(test_poly, extension=ext)[1]
                        has_linear = any(sp.degree(f[0], x) == 1 for f in factors)
                        if not has_linear:
                            neg_q = True
                            break
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: F_qn is the field extension of F_q of degree n",
    "not Q: minimal polynomials do not match all irreducible polynomials"
]

N_HYP = 2
NEG_Q_INDEX = 2