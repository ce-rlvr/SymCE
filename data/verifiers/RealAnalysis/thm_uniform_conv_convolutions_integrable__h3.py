import sympy as sp

x = sp.Symbol('x', real=True)
y = sp.Symbol('y', real=True)
n = sp.Symbol('n', real=True, positive=True)

CONDITION_LABELS = [
    "H_1: (f_n) is a sequence of bounded measurable real-valued functions on R",
    "H_2: (f_n) converges uniformly to a bounded measurable function f on R",
    "¬Q: The sequence of convolutions (f_n * g)(x) does not converge uniformly to (f * g)(x) on R"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    witness is expected to be a tuple of three sympy expressions: (f_n, f, g)
    Example of a valid counterexample witness:
        f_n = 1/n * sp.exp(-x**2 / n**2)
        f = 0
        g = 1
    """
    try:
        if len(witness) != 3:
            return [False, False, False]
        f_n, f, g = witness
    except Exception:
        return [False, False, False]
        
    # H1: f_n is bounded
    try:
        h1 = True
        for n_val in [1, 2, 3]:
            expr_sub = f_n.subs(n, n_val)
            if expr_sub.has(x):
                L1 = sp.limit(expr_sub, x, sp.oo)
                L2 = sp.limit(expr_sub, x, -sp.oo)
                if L1.has(sp.oo) or L1.has(-sp.oo) or L2.has(sp.oo) or L2.has(-sp.oo):
                    h1 = False
                
                try:
                    sings = sp.singularities(expr_sub, x)
                    if sings != sp.S.EmptySet:
                        h1 = False
                except Exception:
                    pass
            else:
                if expr_sub in [sp.oo, -sp.oo, sp.nan, sp.zoo]:
                    h1 = False
    except Exception:
        h1 = False

    # H2: f_n converges uniformly to f, and f is bounded
    try:
        h2 = True
        # Check f is bounded
        if f.has(x):
            L1 = sp.limit(f, x, sp.oo)
            L2 = sp.limit(f, x, -sp.oo)
            if L1.has(sp.oo) or L1.has(-sp.oo) or L2.has(sp.oo) or L2.has(-sp.oo):
                h2 = False
            try:
                sings = sp.singularities(f, x)
                if sings != sp.S.EmptySet:
                    h2 = False
            except Exception:
                pass
        else:
            if f in [sp.oo, -sp.oo, sp.nan, sp.zoo]:
                h2 = False
                
        if h2:
            diff_expr = sp.simplify(f_n - f)
            if not diff_expr.has(x):
                L = sp.limit(diff_expr, n, sp.oo)
                if L != 0:
                    h2 = False
            else:
                L = sp.limit(diff_expr, n, sp.oo)
                if L != 0:
                    h2 = False
                else:
                    try:
                        deriv = sp.diff(diff_expr, x)
                        crit_points = sp.solve(deriv, x)
                        for cp in crit_points:
                            if cp.is_real is not False:
                                val = diff_expr.subs(x, cp)
                                L_cp = sp.limit(val, n, sp.oo)
                                if L_cp != 0:
                                    h2 = False
                                    break
                    except Exception:
                        pass
                    
                    if h2:
                        L_n = sp.limit(diff_expr.subs(x, n), n, sp.oo)
                        L_0 = sp.limit(diff_expr.subs(x, 0), n, sp.oo)
                        if L_n != 0 or L_0 != 0:
                            h2 = False
    except Exception:
        h2 = False

    # neg_Q: f_n * g does NOT converge uniformly to f * g
    try:
        integrand_n = f_n.subs(x, x - y) * g.subs(x, y)
        integrand_f = f.subs(x, x - y) * g.subs(x, y)
        
        conv_n = sp.integrate(integrand_n, (y, -sp.oo, sp.oo))
        conv_f = sp.integrate(integrand_f, (y, -sp.oo, sp.oo))
        
        if conv_n in [sp.oo, -sp.oo, sp.nan, sp.zoo] or str(conv_n) in ['oo', '-oo', 'nan', 'zoo']:
            neg_q = True
        elif conv_n.has(sp.Integral):
            # If integration fails, try evaluating at x=0
            val_n = sp.integrate(integrand_n.subs(x, 0), (y, -sp.oo, sp.oo))
            val_f = sp.integrate(integrand_f.subs(x, 0), (y, -sp.oo, sp.oo))
            if val_n in [sp.oo, -sp.oo, sp.nan, sp.zoo] or str(val_n) in ['oo', '-oo', 'nan', 'zoo']:
                neg_q = True
            elif val_n.has(sp.Integral):
                neg_q = False
            else:
                L_conv = sp.limit(val_n - val_f, n, sp.oo)
                neg_q = (L_conv != 0)
        else:
            diff_conv = sp.simplify(conv_n - conv_f)
            if not diff_conv.has(x):
                L_conv = sp.limit(diff_conv, n, sp.oo)
                neg_q = (L_conv != 0)
            else:
                L_conv = sp.limit(diff_conv, n, sp.oo)
                if L_conv != 0:
                    neg_q = True
                else:
                    neg_q = False
                    try:
                        deriv_conv = sp.diff(diff_conv, x)
                        crit_points_conv = sp.solve(deriv_conv, x)
                        for cp in crit_points_conv:
                            if cp.is_real is not False:
                                val = diff_conv.subs(x, cp)
                                L_cp = sp.limit(val, n, sp.oo)
                                if L_cp != 0:
                                    neg_q = True
                                    break
                    except Exception:
                        pass
                    
                    if not neg_q:
                        L_conv_n = sp.limit(diff_conv.subs(x, n), n, sp.oo)
                        L_conv_0 = sp.limit(diff_conv.subs(x, 0), n, sp.oo)
                        if L_conv_n != 0 or L_conv_0 != 0:
                            neg_q = True
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]