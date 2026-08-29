import sympy
from sympy import Poly
from sympy.abc import x

CONDITION_LABELS = ["H_1: L is a field extension of Q", "H_2: H is a characteristic subgroup of G", "not Q: The fixed field L^H is NOT a normal extension of Q"]
N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            poly_expr = witness[0]
        else:
            poly_expr = witness
            
        if not isinstance(poly_expr, sympy.Expr):
            return [False, False, False]
            
        x_syms = list(poly_expr.free_symbols)
        if len(x_syms) != 1:
            return [False, False, False]
        x_var = x_syms[0]
        poly = Poly(poly_expr, x_var, domain='QQ')
    except Exception:
        return [False, False, False]
        
    try:
        h1 = bool(poly.is_irreducible)
    except Exception:
        h1 = False
        
    h2 = False
    try:
        if isinstance(witness, tuple) and len(witness) >= 2:
            H_obj = witness[1]
            if isinstance(H_obj, list) and len(H_obj) == 1:
                h2 = True
            elif hasattr(H_obj, 'order') and H_obj.order() == 1:
                h2 = True
            elif hasattr(H_obj, 'is_trivial') and H_obj.is_trivial:
                h2 = True
            elif H_obj == 1 or H_obj == [1]:
                h2 = True
        else:
            h2 = True
    except Exception:
        h2 = False
        
    try:
        rr = sympy.real_roots(poly_expr)
        rr_count = len(rr)
        deg = poly.degree()
        
        if 0 < rr_count < deg:
            neg_q = True
        else:
            if deg > 5:
                neg_q = False
            else:
                from sympy import RootOf, AlgebraicNumber, factor_list
                r = RootOf(poly_expr, 0)
                a = AlgebraicNumber(r)
                factors = factor_list(poly_expr, extension=a)[1]
                neg_q = any(fac.as_poly(x_var).degree() > 1 for fac, mult in factors)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]