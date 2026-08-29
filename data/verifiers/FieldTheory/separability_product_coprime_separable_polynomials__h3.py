import sympy
from sympy import Poly, diff, gcd
from sympy.abc import x, y, z, t

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        f, g = witness
    except Exception:
        return [False, False, False]
        
    try:
        f_expr = sympy.sympify(f)
        g_expr = sympy.sympify(g)
        symbols = f_expr.free_symbols | g_expr.free_symbols
        if len(symbols) == 1:
            gen = list(symbols)[0]
        elif len(symbols) == 0:
            gen = x
        else:
            gen = x
            
        poly_f = Poly(f_expr, gen)
        poly_g = Poly(g_expr, gen)
        h1_ok = True
    except Exception:
        h1_ok = False

    try:
        df = diff(f_expr, gen)
        gcd_f = gcd(f_expr, df)
        f_sep = Poly(gcd_f, gen).degree() == 0
        
        dg = diff(g_expr, gen)
        gcd_g = gcd(g_expr, dg)
        g_sep = Poly(gcd_g, gen).degree() == 0
        
        h2_ok = bool(f_sep and g_sep)
    except Exception:
        h2_ok = False

    try:
        fg = f_expr * g_expr
        dfg = diff(fg, gen)
        gcd_fg = gcd(fg, dfg)
        neg_q_ok = bool(Poly(gcd_fg, gen).degree() > 0)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: f and g are separable polynomials",
    "¬Q: f times g is not a separable polynomial"
]

N_HYP = 2
NEG_Q_INDEX = 2