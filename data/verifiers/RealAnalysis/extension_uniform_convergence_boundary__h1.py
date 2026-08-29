import sympy as sp
from sympy.abc import x, n
import math

CONDITION_LABELS = [
    "H_1: f is a continuous real-valued function defined on the closed interval",
    "H_2: The sequence f_n converges uniformly to f on the open interval",
    "not Q: The sequence f_n does not converge uniformly to f on the closed interval"
]
N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        f_expr, fn_expr, a, b = witness
        f_expr = sp.sympify(f_expr)
        fn_expr = sp.sympify(fn_expr)
        a = sp.sympify(a)
        b = sp.sympify(b)
    except Exception:
        return [False, False, False]
        
    # H1: f is continuous on the closed interval
    h1 = False
    try:
        if f_expr.is_constant() or f_expr.is_polynomial(x):
            h1 = True
        else:
            is_cont = True
            pts = [
                a + (b - a) * sp.Rational(1, 2),
                a + (b - a) * sp.Rational(1, 3),
                a + (b - a) * sp.Rational(2, 3),
                a + (b - a) * sp.Rational(1, 4),
                a + (b - a) * sp.Rational(3, 4)
            ]
            for pt in pts:
                lim_plus = sp.limit(f_expr, x, pt, dir='+')
                lim_minus = sp.limit(f_expr, x, pt, dir='-')
                val = f_expr.subs(x, pt)
                if sp.simplify(lim_plus - val) != 0 or sp.simplify(lim_minus - val) != 0:
                    is_cont = False
                    break
            if is_cont:
                if sp.simplify(sp.limit(f_expr, x, a, dir='+') - f_expr.subs(x, a)) != 0:
                    is_cont = False
                if sp.simplify(sp.limit(f_expr, x, b, dir='-') - f_expr.subs(x, b)) != 0:
                    is_cont = False
            h1 = is_cont
    except Exception:
        h1 = False
            
    # H2: fn converges uniformly to f on the open interval
    h2 = False
    try:
        expr = sp.Abs(fn_expr - f_expr)
        
        def get_sup(n_val):
            expr_n = expr.subs(n, n_val)
            inside_n = (fn_expr - f_expr).subs(n, n_val)
            pts = []
            a_f = float(a)
            b_f = float(b)
            
            grid_size = 500
            for i in range(1, grid_size):
                pts.append(a_f + (b_f - a_f) * i / float(grid_size))
                
            for k in range(1, 15):
                delta = (b_f - a_f) * (10 ** (-k / 2.0))
                pts.append(a_f + delta)
                pts.append(b_f - delta)
                
            try:
                deriv = sp.diff(inside_n, x)
                crit_pts = sp.solve(deriv, x)
                for cp in crit_pts:
                    try:
                        cp_f = float(cp)
                        if a_f < cp_f < b_f:
                            pts.append(cp_f)
                    except Exception:
                        pass
            except Exception:
                pass

            max_val = 0.0
            for p in pts:
                try:
                    val_expr = expr_n.subs(x, p)
                    try:
                        val = float(val_expr)
                    except Exception:
                        val = abs(complex(val_expr))
                    if val > max_val:
                        max_val = val
                except Exception:
                    pass
            return max_val

        max_100 = get_sup(100)
        max_1000 = get_sup(1000)
        
        if max_1000 < 1e-4:
            h2 = True
        elif max_1000 > max_100 * 0.9 and max_1000 > 1e-3:
            h2 = False
        else:
            max_10000 = get_sup(10000)
            if max_10000 < 1e-4:
                h2 = True
            elif max_10000 > max_1000 * 0.9 and max_10000 > 1e-3:
                h2 = False
            else:
                max_100000 = get_sup(100000)
                if max_100000 < 1e-3:
                    h2 = True
                else:
                    h2 = False
    except Exception:
        h2 = False

    # neg_Q: fn does NOT converge uniformly to f on the closed interval
    neg_q = False
    try:
        for pt in [a, b]:
            evaluated_analytically = False
            try:
                f_val = f_expr.subs(x, pt)
                fn_val = fn_expr.subs(x, pt)
                lim = sp.limit(fn_val, n, sp.oo)
                
                if lim.has(sp.Limit):
                    raise ValueError("Limit unevaluated")
                    
                if lim.has(sp.AccumBounds):
                    neg_q = True
                    evaluated_analytically = True
                    break
                    
                diff = sp.simplify(lim - f_val)
                if diff != 0:
                    try:
                        if abs(float(diff)) > 1e-7:
                            neg_q = True
                            evaluated_analytically = True
                            break
                    except Exception:
                        neg_q = True
                        evaluated_analytically = True
                        break
                else:
                    evaluated_analytically = True
            except Exception:
                pass
                
            if not evaluated_analytically:
                try:
                    f_val_num = float(f_expr.subs(x, pt))
                    fn_val_10000 = float(fn_expr.subs({x: pt, n: 10000}))
                    if abs(fn_val_10000 - f_val_num) > 1e-4:
                        neg_q = True
                        break
                except Exception:
                    pass
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]