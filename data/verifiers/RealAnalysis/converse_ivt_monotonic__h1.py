import sympy
import math

x, y, z = sympy.symbols('x y z')

CONDITION_LABELS = [
    "H_1: The function f has the intermediate value property on the interval",
    "¬Q: The function f is not continuous on the interval"
]

N_HYP = 1
NEG_Q_INDEX = 1

def linspace(start, stop, n):
    if n <= 1:
        return [start]
    return [start + i * (stop - start) / (n - 1) for i in range(n)]

def find_root(f_call, target, u, v, grid_pts, tol=1e-4):
    try:
        fu = float(f_call(u)) - target
        fv = float(f_call(v)) - target
    except Exception:
        fu = None
        fv = None
        
    brackets = []
    if fu is not None and fv is not None and fu * fv <= 0:
        brackets.append((u, v, fu, fv))
        
    pts = linspace(min(u, v), max(u, v), grid_pts)
    for i in range(len(pts)-1):
        try:
            fl = float(f_call(pts[i])) - target
            fh = float(f_call(pts[i+1])) - target
        except Exception:
            continue
        if abs(fl) < tol or abs(fh) < tol:
            return True
        if fl * fh <= 0:
            brackets.append((pts[i], pts[i+1], fl, fh))
            
    for (low, high, f_low, f_high) in brackets:
        curr_low, curr_high = low, high
        curr_f_low, curr_f_high = f_low, f_high
        for _ in range(60):
            mid = (curr_low + curr_high) / 2.0
            try:
                f_mid = float(f_call(mid)) - target
            except Exception:
                mid += 1e-9
                try:
                    f_mid = float(f_call(mid)) - target
                except Exception:
                    break
            if abs(f_mid) < tol:
                return True
            if curr_f_low * f_mid <= 0:
                curr_high = mid
                curr_f_high = f_mid
            else:
                curr_low = mid
                curr_f_low = f_mid
        try:
            if abs(float(f_call(curr_low)) - target) < tol or abs(float(f_call(curr_high)) - target) < tol:
                return True
        except Exception:
            pass
            
    return False

def check_ivp_numeric(f_call, a, b, num_pts=20, grid_pts=500):
    pts = linspace(a, b, num_pts)
    valid_pairs = 0
    for i in range(len(pts)):
        for j in range(i+1, len(pts)):
            u = pts[i]
            v = pts[j]
            try:
                fu = float(f_call(u))
                fv = float(f_call(v))
            except Exception:
                continue
            if abs(fu - fv) < 1e-4:
                continue
            valid_pairs += 1
            targets = linspace(min(fu, fv), max(fu, fv), 5)[1:-1]
            for target in targets:
                if not find_root(f_call, target, u, v, grid_pts):
                    return False
    return valid_pairs > 0

def check_continuous_numeric(f_call, a, b):
    pts = linspace(a, b, 1000)
    vals = []
    valid_pts = []
    for p in pts:
        try:
            v = float(f_call(p))
            vals.append(v)
            valid_pts.append(p)
        except Exception:
            pass
            
    if len(vals) < 990:
        return False
        
    max_diff = -1
    max_i = -1
    for i in range(len(vals)-1):
        diff = abs(vals[i+1] - vals[i])
        if diff > max_diff:
            max_diff = diff
            max_i = i
            
    if max_diff < 1e-5:
        return True
        
    u = valid_pts[max_i]
    v = valid_pts[max_i+1]
    fine_pts = linspace(u, v, 100)
    fine_vals = []
    for p in fine_pts:
        try:
            fine_vals.append(float(f_call(p)))
        except Exception:
            pass
            
    if len(fine_vals) < 90:
        return False
        
    fine_max_diff = -1
    for i in range(len(fine_vals)-1):
        diff = abs(fine_vals[i+1] - fine_vals[i])
        if diff > fine_max_diff:
            fine_max_diff = diff
            
    if fine_max_diff > max_diff * 0.5:
        return False
        
    return True

def conditions(witness):
    try:
        f, a, b = witness
        a = float(a)
        b = float(b)
    except Exception:
        return [False, False]
        
    if a >= b:
        return [False, False]
        
    is_cont = None
    f_call = None
    num_pts, grid_pts = 20, 500
    
    if isinstance(f, sympy.Expr):
        symbols = list(f.free_symbols)
        sym_x = symbols[0] if symbols else sympy.Symbol('x')
        try:
            domain = sympy.Interval(a, b)
            is_cont_expr = sympy.continuous_domain(f, sym_x, domain)
            if is_cont_expr == domain:
                is_cont = True
            elif isinstance(is_cont_expr, sympy.Set) and not is_cont_expr.intersection(domain) == domain:
                is_cont = False
        except Exception:
            pass
            
        try:
            f_fast = sympy.lambdify(sym_x, f, modules=['math'])
            works = False
            for pt in [a, b, (a+b)/2]:
                try:
                    float(f_fast(pt))
                    works = True
                    break
                except Exception:
                    pass
            if works:
                f_call = f_fast
            else:
                raise ValueError
        except Exception:
            def f_call_slow(val):
                return float(f.subs(sym_x, val).evalf())
            f_call = f_call_slow
            num_pts, grid_pts = 10, 50
    elif callable(f):
        f_call = f
    else:
        return [False, False]
        
    try:
        valid = False
        for test_pt in [a, b, (a+b)/2]:
            try:
                float(f_call(test_pt))
                valid = True
                break
            except Exception:
                pass
        if not valid:
            return [False, False]
            
        if is_cont is None:
            is_cont = check_continuous_numeric(f_call, a, b)
            
        if is_cont:
            ivp_ok = True
        else:
            ivp_ok = check_ivp_numeric(f_call, a, b, num_pts, grid_pts)
            
        neg_q = not is_cont
        
        return [bool(ivp_ok), bool(neg_q)]
    except Exception:
        return [False, False]