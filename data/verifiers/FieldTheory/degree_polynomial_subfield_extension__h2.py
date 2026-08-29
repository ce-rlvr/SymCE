import sympy as sp

x, y, z = sp.symbols('x y z')
QQ = sp.QQ

def conditions(witness):
    try:
        P_expr = sp.sympify(witness[0])
        f_expr = sp.sympify(witness[1])
        n = int(witness[2])
    except Exception:
        return [False, False]
        
    symbols = P_expr.free_symbols | f_expr.free_symbols
    if len(symbols) == 1:
        var_x = list(symbols)[0]
    elif len(symbols) == 0:
        var_x = x
    else:
        var_x = x if x in symbols else list(symbols)[0]
        
    var_y = sp.Symbol('y_tmp')
    if var_x == var_y:
        var_y = sp.Symbol('z_tmp')
        
    try:
        P_poly = sp.Poly(P_expr, var_x, domain='QQ')
        h1 = bool(P_poly.degree() >= 1 and P_poly.is_irreducible)
    except Exception:
        h1 = False
        
    try:
        f_frac = sp.cancel(f_expr)
        g, h = sp.fraction(f_frac)
        
        P_y = P_expr.subs(var_x, var_y)
        g_y = g.subs(var_x, var_y)
        h_y = h.subs(var_x, var_y)
        
        h_poly = sp.Poly(h, var_x, domain='QQ')
        
        if sp.gcd(P_poly, h_poly).degree() > 0:
            neg_q = False
        else:
            res = sp.resultant(P_y, var_x * h_y - g_y, var_y)
            res_poly = sp.Poly(res, var_x, domain='QQ')
            
            sqf = res_poly.sqf_part()
            deg_beta = sqf.degree()
            deg_alpha = P_poly.degree()
            
            if deg_beta == 0:
                neg_q = False
            else:
                extension_degree = deg_alpha // deg_beta
                neg_q = bool(extension_degree > n)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: L is a finite field extension of K",
    "¬Q: degree of K(alpha) over K(f(alpha)) is greater than n"
]

N_HYP = 1
NEG_Q_INDEX = 1