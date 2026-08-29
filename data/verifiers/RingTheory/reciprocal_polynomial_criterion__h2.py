import sympy

x = sympy.Symbol('x')

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: The constant term a_0 is non-zero",
    "H_3: The reciprocal polynomial is irreducible",
    "not_Q: f is not irreducible"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, dict):
            f_expr = witness.get('f', witness.get('f_expr'))
            n_val = witness.get('n', witness.get('n_val'))
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            f_expr, n_val = witness
        else:
            f_expr = witness
            n_val = None

        var = sympy.Symbol('x')
        
        if isinstance(f_expr, list):
            poly_f = sympy.Poly(f_expr, var, domain='QQ')
            f_expr = poly_f.as_expr()
        else:
            f_expr = sympy.sympify(f_expr)
            syms = f_expr.free_symbols
            if len(syms) == 1:
                var = list(syms)[0]
            elif len(syms) > 1:
                return [False, False, False, False]
            else:
                var = sympy.Symbol('x')
            poly_f = sympy.Poly(f_expr, var, domain='QQ')

        if n_val is None:
            n_val = poly_f.degree()
        else:
            n_val = int(n_val)

        h1 = True

        try:
            a0 = poly_f.eval(0)
            h2 = bool(a0 != 0)
        except Exception:
            h2 = False

        try:
            f_star_expr = sympy.expand((var**n_val) * f_expr.subs(var, 1/var))
            poly_f_star = sympy.Poly(f_star_expr, var, domain='QQ')
            h3 = bool(poly_f_star.is_irreducible)
        except Exception:
            h3 = False

        try:
            neg_q = not bool(poly_f.is_irreducible)
        except Exception:
            neg_q = False

        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]