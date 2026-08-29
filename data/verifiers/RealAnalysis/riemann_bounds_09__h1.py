import sympy
from sympy import Symbol, Rational, Integer
from sympy.abc import x, y, z, t

CONDITION_LABELS = [
    "H_1: f and g are either both monotonically increasing or both monotonically decreasing on the interval",
    "neg_Q: (Integral f) * (Integral g) > (b - a) * Integral f g"
]

N_HYP = 1
NEG_Q_INDEX = 1

def get_symbols(f, g):
    symbols = set()
    if hasattr(f, 'free_symbols'):
        symbols.update(f.free_symbols)
    if hasattr(g, 'free_symbols'):
        symbols.update(g.free_symbols)
    if len(symbols) == 1:
        return list(symbols)[0]
    elif len(symbols) == 0:
        return sympy.Symbol('x')
    else:
        x_sym = sympy.Symbol('x')
        if x_sym in symbols:
            return x_sym
        return list(symbols)[0]

def conditions(witness):
    try:
        if len(witness) == 5:
            f, g, var, a, b = witness
        elif len(witness) == 4:
            f, g, a, b = witness
            var = get_symbols(f, g)
        else:
            return [False, False]
    except Exception:
        return [False, False]

    # H1: f and g are either both monotonically increasing or both monotonically decreasing on the interval
    h1_ok = False
    try:
        a_val = float(a)
        b_val = float(b)
        
        if a_val >= b_val:
            h1_ok = True
        else:
            def check_mono(expr, direction):
                df = sympy.diff(expr, var)
                if df == 0:
                    return True
                try:
                    roots = sympy.solve(df, var)
                except Exception:
                    roots = []
                
                crit_points = [a_val, b_val]
                for r in roots:
                    try:
                        if r.is_real and a_val <= float(r) <= b_val:
                            crit_points.append(float(r))
                    except Exception:
                        pass
                
                crit_points = sorted(list(set(crit_points)))
                test_points = []
                for i in range(len(crit_points)-1):
                    test_points.append((crit_points[i] + crit_points[i+1]) / 2.0)
                test_points.extend(crit_points)
                
                for p in test_points:
                    try:
                        val = float(df.subs(var, p))
                        if direction == 'inc' and val < -1e-9:
                            return False
                        if direction == 'dec' and val > 1e-9:
                            return False
                    except Exception:
                        pass
                return True

            f_inc = check_mono(f, 'inc')
            f_dec = check_mono(f, 'dec')
            g_inc = check_mono(g, 'inc')
            g_dec = check_mono(g, 'dec')
            
            h1_ok = (f_inc and g_inc) or (f_dec and g_dec)
    except Exception:
        h1_ok = False

    # neg_Q: The conclusion fails at the witness
    neg_q_ok = False
    try:
        int_f = sympy.integrate(f, (var, a, b))
        int_g = sympy.integrate(g, (var, a, b))
        int_fg = sympy.integrate(f * g, (var, a, b))
        
        lhs = int_f * int_g
        rhs = (b - a) * int_fg
        
        neg_q_ok = float(lhs) > float(rhs) + 1e-9
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]