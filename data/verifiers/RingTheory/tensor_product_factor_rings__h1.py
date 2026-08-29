import sympy
from sympy import Poly, gcd
from sympy.abc import x, y, z, t, u, v, w

def are_isomorphic(f, g):
    try:
        f_expr = sympy.sympify(f)
        g_expr = sympy.sympify(g)
    except Exception:
        return False
        
    vars_f = f_expr.free_symbols
    vars_g = g_expr.free_symbols
    
    common_vars = vars_f.intersection(vars_g)
    if not common_vars:
        return True
        
    var = list(common_vars)[0]
    
    try:
        poly_f = sympy.Poly(f_expr, var)
        poly_g = sympy.Poly(g_expr, var)
    except Exception:
        return False
        
    if poly_f.is_zero and poly_g.is_zero:
        return False
        
    if poly_f.is_zero:
        return poly_g.degree() == 0
        
    if poly_g.is_zero:
        return poly_f.degree() == 0
        
    deg_f = poly_f.degree()
    deg_g = poly_g.degree()
    
    h = sympy.gcd(f_expr, g_expr)
    poly_h = sympy.Poly(h, var)
    deg_gcd = poly_h.degree()
    
    return deg_f * deg_g == deg_gcd

def conditions(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        f, g = witness
    except Exception:
        return [False, False, False]
        
    # H1: f is a polynomial
    try:
        if isinstance(f, (int, float)):
            h1 = True
        elif hasattr(f, 'free_symbols'):
            syms_f = f.free_symbols
            if len(syms_f) > 1:
                h1 = False
            elif len(syms_f) == 1:
                sympy.Poly(f, *syms_f)
                h1 = True
            else:
                h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # H2: g is a polynomial
    try:
        if isinstance(g, (int, float)):
            h2 = True
        elif hasattr(g, 'free_symbols'):
            syms_g = g.free_symbols
            if len(syms_g) > 1:
                h2 = False
            elif len(syms_g) == 1:
                sympy.Poly(g, *syms_g)
                h2 = True
            else:
                h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: conclusion fails
    try:
        neg_q = not are_isomorphic(f, g)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a polynomial",
    "H_2: g is a polynomial",
    "¬Q: Tensor product is not isomorphic to quotient ring"
]

N_HYP = 2
NEG_Q_INDEX = 2