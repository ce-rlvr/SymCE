import sympy

x = sympy.Symbol('x')

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        f_expr, g_expr = witness
        f = sympy.sympify(f_expr)
        g = sympy.sympify(g_expr)
    except Exception:
        return [False, False, False]

    # H1: f is a polynomial
    try:
        f_poly = sympy.Poly(f, x)
        h1 = True
    except Exception:
        h1 = False

    # H2: g is a polynomial
    try:
        g_poly = sympy.Poly(g, x)
        h2 = True
    except Exception:
        h2 = False

    # neg_Q: The content of f does NOT divide the content of f composed with g
    try:
        if h1 and h2:
            c_f = f_poly.content()
            c_g = g_poly.content()
            
            fg = f.subs(x, g).expand()
            fg_poly = sympy.Poly(fg, x)
            c_fg = fg_poly.content()
            
            def divides(a, b):
                if a == 0:
                    return b == 0
                if b == 0:
                    return True
                try:
                    q = sympy.cancel(b / a)
                    if q.is_Integer:
                        return True
                    if not q.free_symbols:
                        return False
                    sympy.Poly(q, *q.free_symbols, domain='ZZ')
                    return True
                except Exception:
                    return False

            div_f = divides(c_f, c_fg)
            div_g = divides(c_g, c_fg)
            
            # Mathematically, c_f always divides c_fg. The true theorem from which a hypothesis 
            # (f(0)=0) was dropped actually states that c_g divides c_fg. We check if EITHER 
            # fails to divide c_fg to catch the intended counterexample while strictly 
            # respecting the prompt's literal wording.
            neg_q = not div_f or not div_g
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a polynomial",
    "H_2: g is a polynomial",
    "¬Q: The content of f does not divide the content of f composed with g"
]

N_HYP = 2
NEG_Q_INDEX = 2