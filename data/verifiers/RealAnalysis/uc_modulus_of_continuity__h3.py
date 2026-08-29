import sympy as sp
import math

# Top-level setup
x = sp.Symbol('x', real=True)
t = sp.Symbol('t', real=True, nonnegative=True)
n = sp.Symbol('n', integer=True, positive=True)

def _get_evaluator(obj, sym):
    if callable(obj):
        return lambda val: float(obj(val))
    else:
        expr = sp.sympify(obj)
        return lambda val: float(expr.subs(sym, val))

def conditions(witness) -> list[bool]:
    """
    Expected witness dictionary format:
    {
        'domain': sp.Set (optional, defaults to sp.S.Reals),
        'f': sympy expression in x (or callable),
        'omega': sympy expression in t (or callable),
        'x_n': sympy expression in n (or callable),
        'y_n': sympy expression in n (or callable)
    }
    """
    
    # H_1: (X, d_X) and (Y, d_Y) are metric spaces
    try:
        domain = witness.get('domain', sp.S.Reals)
        h1 = isinstance(domain, sp.Set) or domain == 'R' or domain == 'Reals'
    except Exception:
        h1 = False

    # H_2: f: X -> Y is a function
    try:
        f_eval = _get_evaluator(witness['f'], x)
        h2 = False
        for pt in [0.0, 1.0, 2.0, 3.14159]:
            try:
                val = f_eval(pt)
                if isinstance(val, float) and not math.isnan(val) and not math.isinf(val):
                    h2 = True
                    break
            except Exception:
                pass
    except Exception:
        h2 = False

    # H_3: d_Y(f(x), f(y)) <= omega(d_X(x, y)) for all x, y in X
    try:
        f_eval = _get_evaluator(witness['f'], x)
        omega_eval = _get_evaluator(witness['omega'], t)
        xn_eval = _get_evaluator(witness['x_n'], n)
        yn_eval = _get_evaluator(witness['y_n'], n)
        
        domain = witness.get('domain', sp.S.Reals)
        
        test_points = [0.0, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0, -0.1, -0.5, -1.0, -2.0, -5.0, -10.0]
        
        for n_val in [1, 10, 100, 1000]:
            try:
                test_points.append(xn_eval(n_val))
                test_points.append(yn_eval(n_val))
            except Exception:
                pass
                
        if isinstance(domain, sp.Set):
            valid_points = []
            for pt in test_points:
                try:
                    if domain.contains(pt) != False:
                        valid_points.append(pt)
                except Exception:
                    pass
            test_points = valid_points
            
        test_points = list(set(test_points))
        
        h3 = True
        for a in test_points:
            for b in test_points:
                dist_x = abs(a - b)
                try:
                    fa = f_eval(a)
                    fb = f_eval(b)
                    if math.isinf(fa) or math.isnan(fa) or math.isinf(fb) or math.isnan(fb):
                        continue
                    
                    dist_y = abs(fa - fb)
                    om_val = omega_eval(dist_x)
                    
                    if math.isinf(om_val) or math.isnan(om_val):
                        h3 = False
                        break
                        
                    if dist_y > om_val + 1e-5:
                        h3 = False
                        break
                except Exception:
                    pass
            if not h3:
                break
    except Exception:
        h3 = False

    # neg_Q: f is not uniformly continuous on X
    try:
        f_eval = _get_evaluator(witness['f'], x)
        xn_eval = _get_evaluator(witness['x_n'], n)
        yn_eval = _get_evaluator(witness['y_n'], n)
        
        cond_lim_diff = True
        cond_lim_f = True
        
        diffs_x = []
        diffs_f = []
        
        for n_val in [100, 1000, 10000, 100000]:
            try:
                xn_val = xn_eval(n_val)
                yn_val = yn_eval(n_val)
                if math.isinf(xn_val) or math.isnan(xn_val) or math.isinf(yn_val) or math.isnan(yn_val):
                    continue
                diffs_x.append(abs(xn_val - yn_val))
                
                fxn_val = f_eval(xn_val)
                fyn_val = f_eval(yn_val)
                if math.isinf(fxn_val) or math.isnan(fxn_val) or math.isinf(fyn_val) or math.isnan(fyn_val):
                    continue
                diffs_f.append(abs(fxn_val - fyn_val))
            except Exception:
                pass
                
        if len(diffs_x) < 2:
            neg_q = False
        else:
            if diffs_x[-1] > 1e-2:
                cond_lim_diff = False
                
            if max(diffs_f) < 1e-2:
                cond_lim_f = False
                
            neg_q = cond_lim_diff and cond_lim_f
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: (X, d_X) and (Y, d_Y) are metric spaces",
    "H_2: f: X -> Y is a function",
    "H_3: d_Y(f(x), f(y)) <= omega(d_X(x, y)) for all x, y in X",
    "¬Q: f is not uniformly continuous on X"
]

N_HYP = 3
NEG_Q_INDEX = 3