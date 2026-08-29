import sympy

x = sympy.Symbol('x')
I = sympy.I

def conditions(witness):
    # H_1: The degree of P(x) is an odd integer
    try:
        expr = sympy.sympify(witness)
        if hasattr(expr, 'free_symbols') and len(expr.free_symbols - {x}) > 0:
            h1_ok = False
        else:
            poly = sympy.Poly(expr, x)
            deg = poly.degree()
            h1_ok = (deg % 2 == 1)
    except Exception:
        h1_ok = False

    # ¬Q: There does NOT exist a real number c such that P(c) = 0
    try:
        expr = sympy.sympify(witness)
        poly = sympy.Poly(expr, x)
        try:
            roots = poly.nroots()
        except Exception:
            roots = sympy.solve(expr, x)
            
        has_real_root = False
        for r in roots:
            try:
                r_c = complex(r)
                if abs(r_c.imag) < 1e-9:
                    has_real_root = True
                    break
            except Exception:
                if getattr(r, 'is_real', False) is True:
                    has_real_root = True
                    break
                elif getattr(r, 'is_real', None) is None:
                    try:
                        r_eval = r.evalf()
                        if abs(sympy.im(r_eval)) < 1e-9:
                            has_real_root = True
                            break
                    except Exception:
                        pass
        neg_q_ok = not has_real_root
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: The degree of P(x) is an odd integer",
    "¬Q: There does not exist a real number c such that P(c) = 0"
]

N_HYP = 1
NEG_Q_INDEX = 1