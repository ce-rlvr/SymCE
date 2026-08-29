import sympy
from sympy.abc import x, y, z, t

def conditions(witness):
    try:
        if len(witness) != 2:
            return [False, False]
        f, g = witness
    except Exception:
        return [False, False]
        
    try:
        f_expr = sympy.sympify(f)
        g_expr = sympy.sympify(g)
        
        syms = f_expr.free_symbols | g_expr.free_symbols
        var = sympy.Symbol('x')
        if var not in syms:
            if len(syms) > 0:
                var = sorted(list(syms), key=lambda s: s.name)[0]
            else:
                var = sympy.Symbol('x')
                
        f_poly = sympy.Poly(f_expr, var)
        g_poly = sympy.Poly(g_expr, var)
        
        h1 = bool(f_poly.degree() > 0 and g_poly.degree() > 0)
    except Exception:
        h1 = False

    try:
        gb = sympy.groebner([f_expr, g_expr], var)
        
        is_zero_ring = False
        for p in gb:
            if p.as_expr() in [1, -1]:
                is_zero_ring = True
                break
                
        res = sympy.resultant(f_expr, g_expr, var)
        res_not_zero = bool(res != 0)
        
        neg_q = bool(is_zero_ring != res_not_zero)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = ["H_1: f and g are non-constant polynomials", "not_Q: factor ring is zero ring iff Res != 0 fails"]
N_HYP = 1
NEG_Q_INDEX = 1