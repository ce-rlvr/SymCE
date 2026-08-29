import sympy as sp
import math

x = sp.Symbol('x')
y = sp.Symbol('y')
z = sp.Symbol('z')
t = sp.Symbol('t')

CONDITION_LABELS = [
    "H_1: f is a continuous real-valued function on the closed interval a to b",
    "not Q: The integral bound fails"
]

N_HYP = 1
NEG_Q_INDEX = 1

def check_H1(f_expr, x_var, a, b):
    try:
        a_f = float(a)
        b_f = float(b)
        if a_f >= b_f:
            return False
    except Exception:
        return False
        
    try:
        from sympy.calculus.util import continuous_domain
        from sympy import Interval
        domain = continuous_domain(f_expr, x_var, sp.S.Reals)
        interval = Interval(a, b)
        if interval.is_subset(domain) == True:
            return True
    except Exception:
        pass
        
    try:
        f_lamb = sp.lambdify(x_var, f_expr, modules=['math'])
        N_pts = 10000
        step = (b_f - a_f) / N_pts
        
        def safe_eval(x_val):
            try:
                y_val = float(f_lamb(x_val))
                if math.isnan(y_val) or math.isinf(y_val):
                    return None
                return y_val
            except Exception:
                return None

        prev_y = safe_eval(a_f + 1e-9)
        if prev_y is None:
            return False
            
        for i in range(1, N_pts):
            x_val = a_f + i * step
            y_val = safe_eval(x_val)
            if y_val is None:
                y_val = safe_eval(x_val + 1e-9)
                if y_val is None:
                    return False
            if abs(y_val - prev_y) > 0.5:
                mid_y = safe_eval(x_val - step/2)
                if mid_y is not None:
                    if min(abs(mid_y - prev_y), abs(y_val - mid_y)) < 0.1 * abs(y_val - prev_y):
                        return False
            prev_y = y_val
        return True
    except Exception:
        return False

def check_neg_Q(f_expr, x_var, a, b):
    try:
        a_f = float(a)
        b_f = float(b)
    except Exception:
        return False
        
    try:
        f_lamb = sp.lambdify(x_var, f_expr, modules=['math'])
    except Exception:
        return False

    def safe_eval(x_val):
        try:
            y_val = float(f_lamb(x_val))
            if math.isnan(y_val) or math.isinf(y_val):
                y_val = float(f_lamb(x_val + 1e-10))
                if math.isnan(y_val) or math.isinf(y_val):
                    return 0.0
            return y_val
        except Exception:
            try:
                y_val = float(f_lamb(x_val + 1e-10))
                if math.isnan(y_val) or math.isinf(y_val):
                    return 0.0
                return y_val
            except Exception:
                return 0.0

    def compute_var(N):
        step_v = (b_f - a_f) / N
        var = 0.0
        prev_y = safe_eval(a_f)
        for i in range(1, N + 1):
            x_val = a_f + i * step_v
            y_val = safe_eval(x_val)
            var += abs(y_val - prev_y)
            prev_y = y_val
        return var

    try:
        # Compute LHS
        N_int = 10000
        step_int = (b_f - a_f) / N_int
        integral = 0.0
        for i in range(N_int):
            x_val = a_f + (i + 0.5) * step_int
            integral += safe_eval(x_val) * step_int
        fa = safe_eval(a_f)
        LHS = abs(integral - fa * (b_f - a_f))
        
        # Compute RHS (approximate with N=10000)
        RHS_approx = compute_var(10000) * (b_f - a_f)
        
        if LHS > RHS_approx + 1e-5:
            return True

        # Check for unbounded variation
        v_1k = compute_var(1000)
        v_2k = compute_var(2000)
        v_4k = compute_var(4000)
        v_8k = compute_var(8000)
        
        D1 = v_2k - v_1k
        D2 = v_4k - v_2k
        D3 = v_8k - v_4k
        
        if D3 > 1e-4 and D2 > 1e-4:
            if D3 > 0.8 * D2 and D2 > 0.8 * D1:
                return True
                
        return False
    except Exception:
        return False

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                f_expr, a, b = witness
                free = getattr(f_expr, 'free_symbols', set())
                x_var = list(free)[0] if free else sp.Symbol('x')
            elif len(witness) == 4:
                f_expr, x_var, a, b = witness
            else:
                return [False, False]
        else:
            return [False, False]
            
        h1 = check_H1(f_expr, x_var, a, b)
        neg_q = check_neg_Q(f_expr, x_var, a, b)
        
        return [h1, neg_q]
    except Exception:
        return [False, False]