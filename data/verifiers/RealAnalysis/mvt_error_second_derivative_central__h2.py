import sympy as sp
from sympy.abc import t
import math

def is_diff_4_exists(f, t_sym, c_val):
    try:
        f3 = sp.diff(f, t_sym, 3)
        h_sym = sp.Symbol('h_sym', positive=True)
        
        f3_right = f3.subs(t_sym, c_val + h_sym)
        f3_c = f3.subs(t_sym, c_val)
        f3_left = f3.subs(t_sym, c_val - h_sym)
        
        dq_right = (f3_right - f3_c) / h_sym
        dq_left = (f3_c - f3_left) / h_sym
        
        lim_right = sp.limit(dq_right, h_sym, 0, dir='+')
        lim_left = sp.limit(dq_left, h_sym, 0, dir='+')
        
        if lim_right == lim_left:
            return lim_right.is_real
        else:
            diff = abs(float(lim_right) - float(lim_left))
            return diff < 1e-6
    except Exception:
        return False

def conditions(witness):
    try:
        f, x, h = witness
        h_val = float(h)
        h1_ok = h_val > 0
    except Exception:
        h1_ok = False
        
    try:
        f, x, h = witness
        
        f_x_plus_h = f.subs(t, x + h)
        f_x = f.subs(t, x)
        f_x_minus_h = f.subs(t, x - h)
        
        f_prime2 = sp.diff(f, t, 2)
        f_prime2_x = f_prime2.subs(t, x)
        
        LHS = (f_x_plus_h - 2*f_x + f_x_minus_h) / (h**2) - f_prime2_x
        
        c = sp.Symbol('c', real=True)
        f4 = sp.diff(f, t, 4)
        RHS = (h**2 / 12) * f4.subs(t, c)
        eq = sp.Eq(LHS, RHS)
        
        def check_c(c_val):
            try:
                if not is_diff_4_exists(f, t, c_val):
                    return False
                rhs_val = RHS.subs(c, c_val)
                diff = float(sp.Abs(LHS - rhs_val).evalf())
                lhs_mag = float(sp.Abs(LHS).evalf())
                if lhs_mag > 1:
                    return diff / lhs_mag < 1e-6
                else:
                    return diff < 1e-6
            except Exception:
                return False

        lower = float(x - abs(h))
        upper = float(x + abs(h))

        sols = sp.solveset(eq, c, domain=sp.S.Reals)
        
        fallback = False
        if sols == sp.S.EmptySet:
            neg_q = True
        elif isinstance(sols, sp.FiniteSet):
            any_valid = False
            for sol in sols:
                try:
                    sol_val = float(sol.evalf())
                    if lower < sol_val < upper:
                        if check_c(sol):
                            any_valid = True
                            break
                except Exception:
                    pass
            neg_q = not any_valid
        elif isinstance(sols, (sp.Interval, sp.Union)) and not isinstance(sols, sp.FiniteSet):
            intersected = sp.Intersection(sols, sp.Interval.open(lower, upper))
            if intersected == sp.S.EmptySet:
                neg_q = True
            else:
                intervals = intersected.args if isinstance(intersected, sp.Union) else [intersected]
                any_valid = False
                for interval in intervals:
                    if isinstance(interval, sp.Interval):
                        try:
                            mid = float((interval.start + interval.end) / 2)
                            if check_c(mid):
                                any_valid = True
                                break
                        except Exception:
                            pass
                    elif isinstance(interval, sp.FiniteSet):
                        for sol in interval:
                            try:
                                sol_val = float(sol.evalf())
                                if lower < sol_val < upper:
                                    if check_c(sol):
                                        any_valid = True
                                        break
                            except Exception:
                                pass
                neg_q = not any_valid
        else:
            fallback = True
            
        if fallback:
            neg_q = True
            N = 1000
            c_vals = [lower + i * (upper - lower) / N for i in range(1, N)]
            
            g_vals = []
            try:
                LHS_val = float(LHS.evalf())
                for cv in c_vals:
                    try:
                        gv = float(RHS.subs(c, cv).evalf()) - LHS_val
                        g_vals.append((cv, gv))
                    except Exception:
                        pass
            except Exception:
                pass
            
            for i in range(len(g_vals)):
                cv, gv = g_vals[i]
                if abs(gv) < 1e-6:
                    if check_c(cv):
                        neg_q = False
                        break
                if i > 0:
                    prev_cv, prev_gv = g_vals[i-1]
                    if gv * prev_gv < 0:
                        a, b = prev_cv, cv
                        fa, fb = prev_gv, gv
                        for _ in range(30):
                            mid = (a + b) / 2
                            try:
                                fmid = float(RHS.subs(c, mid).evalf()) - LHS_val
                            except Exception:
                                break
                            if abs(fmid) < 1e-6:
                                if check_c(mid):
                                    neg_q = False
                                break
                            if fa * fmid < 0:
                                b = mid
                                fb = fmid
                            else:
                                a = mid
                                fa = fmid
                        if not neg_q:
                            break
                            
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: h > 0",
    "¬Q: There is no c in (x-h, x+h) such that the error equation holds"
]

N_HYP = 1
NEG_Q_INDEX = 1