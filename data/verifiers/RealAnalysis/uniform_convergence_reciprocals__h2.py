import sympy
from sympy import Symbol, Interval, oo, limit, Abs, diff, solve, Union, FiniteSet
import math

CONDITION_LABELS = [
    "H_1: (f_n) is a sequence of real-valued functions on S that converges uniformly to f on S",
    "¬Q: (1/f_n) does not converge uniformly to 1/f on S"
]
N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        f_n, f, S, x, n = witness
    except Exception:
        return [False, False]

    def check_real_valued(expr):
        def check_n(n_val):
            expr_n = expr.subs(n, n_val)
            pts = []
            if isinstance(S, Interval):
                if S.start.is_real and S.end.is_real:
                    start = float(S.start)
                    end = float(S.end)
                    pts = [(start+end)/2, start + (end-start)/4, start + 3*(end-start)/4]
                elif S.start == -oo and S.end == oo:
                    pts = [0.0, 1.0, -1.0, 3.14, -3.14]
                elif S.start == -oo:
                    end = float(S.end)
                    pts = [end - 1.0, end - 3.14, end - 10.0]
                elif S.end == oo:
                    start = float(S.start)
                    pts = [start + 1.0, start + 3.14, start + 10.0]
            elif isinstance(S, Union):
                for arg in S.args:
                    if isinstance(arg, Interval) and arg.start.is_real and arg.end.is_real:
                        pts.append(float((arg.start + arg.end)/2))
            elif isinstance(S, FiniteSet):
                pts = [float(p) for p in S.args if p.is_real]
            
            if not pts:
                pts = [0.5]
                
            for pt in pts:
                try:
                    c_val = complex(expr_n.subs(x, pt))
                    if abs(c_val.imag) > 1e-9:
                        return False
                except Exception:
                    pass
            return True
        return check_n(10) and check_n(100)

    def check_uniform_convergence(diff_expr):
        # 1. Try symbolic limit of maximum
        try:
            from sympy.calculus.util import maximum
            max_val = maximum(Abs(diff_expr), x, S)
            lim_val = limit(max_val, n, oo)
            if lim_val == 0:
                return True
            elif lim_val > 0 or lim_val == oo:
                return False
        except Exception:
            pass

        # Precompute critical points symbolically if possible
        symbolic_crit_pts = []
        try:
            deriv = diff(diff_expr, x)
            crit_pts = solve(deriv, x)
            for pt in crit_pts:
                symbolic_crit_pts.append(pt)
        except Exception:
            pass

        # 2. Numerical evaluation for large n
        def get_max_for_n(n_val):
            expr_n = diff_expr.subs(n, n_val)
            pts_to_check = []
            
            def add_interval_pts(start, end, is_start_real, is_end_real):
                if is_start_real and is_end_real:
                    start = float(start)
                    end = float(end)
                    pts_to_check.extend([start, end])
                    for i in range(1, 100):
                        pts_to_check.append(start + i * (end - start) / 100.0)
                    for k in range(1, 15):
                        pts_to_check.append(start + 10**(-k) * (end - start))
                        pts_to_check.append(end - 10**(-k) * (end - start))
                elif not is_start_real and not is_end_real:
                    for i in range(-100, 101):
                        pts_to_check.append(float(i))
                    for k in range(1, 15):
                        pts_to_check.append(10**k)
                        pts_to_check.append(-10**k)
                        pts_to_check.append(10**(-k))
                        pts_to_check.append(-10**(-k))
                elif not is_start_real:
                    end = float(end)
                    pts_to_check.append(end)
                    for i in range(1, 100):
                        pts_to_check.append(end - i)
                    for k in range(1, 15):
                        pts_to_check.append(end - 10**k)
                        pts_to_check.append(end - 10**(-k))
                elif not is_end_real:
                    start = float(start)
                    pts_to_check.append(start)
                    for i in range(1, 100):
                        pts_to_check.append(start + i)
                    for k in range(1, 15):
                        pts_to_check.append(start + 10**k)
                        pts_to_check.append(start + 10**(-k))

            if isinstance(S, Interval):
                add_interval_pts(S.start, S.end, S.start.is_real, S.end.is_real)
            elif isinstance(S, Union):
                for arg in S.args:
                    if isinstance(arg, Interval):
                        add_interval_pts(arg.start, arg.end, arg.start.is_real, arg.end.is_real)
                    elif isinstance(arg, FiniteSet):
                        for pt in arg.args:
                            if pt.is_real:
                                pts_to_check.append(float(pt))
            elif isinstance(S, FiniteSet):
                for pt in S.args:
                    if pt.is_real:
                        pts_to_check.append(float(pt))

            for pt_expr in symbolic_crit_pts:
                try:
                    pt_val = pt_expr.subs(n, n_val)
                    if pt_val.is_real:
                        in_S = False
                        try:
                            if S.contains(pt_val):
                                in_S = True
                        except Exception:
                            if isinstance(S, Interval):
                                cond1 = (S.start == -oo) or (pt_val >= S.start)
                                cond2 = (S.end == oo) or (pt_val <= S.end)
                                if cond1 and cond2:
                                    in_S = True
                        if in_S:
                            pts_to_check.append(float(pt_val))
                except Exception:
                    pass

            max_val = -1.0
            for pt in pts_to_check:
                try:
                    c_val = complex(expr_n.subs(x, pt))
                    val = abs(c_val)
                    if val > max_val:
                        max_val = val
                except Exception:
                    pass
            return max_val

        try:
            max_10000 = get_max_for_n(10000)
            max_1000000 = get_max_for_n(1000000)
            
            if max_1000000 != -1.0:
                if max_1000000 < 1e-2:
                    return True
                elif max_1000000 > 1e-1:
                    return False
                elif max_1000000 < max_10000 * 0.5:
                    return True
                else:
                    return False
        except Exception:
            pass
            
        return None

    try:
        h1 = check_real_valued(f_n) and check_real_valued(f) and (check_uniform_convergence(f_n - f) is True)
    except Exception:
        h1 = False

    try:
        res = check_uniform_convergence(1/f_n - 1/f)
        if res is True:
            neg_q = False
        else:
            neg_q = True
    except Exception:
        neg_q = True

    return [h1, neg_q]