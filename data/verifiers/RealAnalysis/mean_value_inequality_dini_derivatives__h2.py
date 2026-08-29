import sympy
import math
from sympy.abc import x

def eval_f(f, x_val):
    if hasattr(f, 'subs'):
        syms = list(f.free_symbols)
        if len(syms) == 1:
            res = f.subs(syms[0], x_val)
        elif len(syms) == 0:
            res = f
        else:
            res = f.subs(x, x_val)
        return float(res)
    return float(f(x_val))

def conditions(witness):
    try:
        if isinstance(witness, dict):
            f = witness['f']
            a = witness['a']
            b = witness['b']
        else:
            f, a, b = witness
    except Exception:
        return [False, False]

    h1_ok = False
    try:
        a_val = float(a)
        b_val = float(b)
        h1_ok = True
        
        if a_val < b_val:
            if hasattr(f, 'free_symbols') and len(f.free_symbols) == 1:
                try:
                    from sympy.calculus.util import continuous_domain
                    from sympy import Interval
                    syms = list(f.free_symbols)
                    dom = continuous_domain(f, syms[0], Interval(a_val, b_val))
                    if dom != Interval(a_val, b_val):
                        h1_ok = False
                except Exception:
                    pass
            
            if h1_ok:
                n = 1000
                dx = (b_val - a_val) / n
                for i in range(n + 1):
                    try:
                        x_val = a_val + dx * i
                        v = eval_f(f, x_val)
                        if math.isnan(v) or math.isinf(v):
                            h1_ok = False
                            break
                    except Exception:
                        h1_ok = False
                        break
        elif a_val == b_val:
            try:
                v = eval_f(f, a_val)
                if math.isnan(v) or math.isinf(v):
                    h1_ok = False
            except Exception:
                h1_ok = False
        else:
            h1_ok = True
            
    except Exception:
        h1_ok = False

    neg_Q = False
    try:
        a_val = float(a)
        b_val = float(b)
        
        if a_val == b_val:
            neg_Q = True
        elif a_val > b_val:
            neg_Q = True
        else:
            fa = eval_f(f, a_val)
            fb = eval_f(f, b_val)
            diff_quot = (fb - fa) / (b_val - a_val)
            
            min_D = float('inf')
            max_D = float('-inf')
            
            n_samples = 1000
            for i in range(1, n_samples):
                x_val = a_val + (b_val - a_val) * i / n_samples
                try:
                    fx = eval_f(f, x_val)
                except Exception:
                    continue
                    
                best_dp = float('-inf')
                for h in [1e-4, 1e-5, 1e-6, 1e-7]:
                    try:
                        fxh = eval_f(f, x_val + h)
                        dp = (fxh - fx) / h
                        if dp > best_dp:
                            best_dp = dp
                    except Exception:
                        pass
                
                if best_dp != float('-inf'):
                    if best_dp < min_D: min_D = best_dp
                    if best_dp > max_D: max_D = best_dp
            
            if diff_quot < min_D - 1e-3 or diff_quot > max_D + 1e-3:
                neg_Q = True
            else:
                neg_Q = False
    except Exception:
        neg_Q = False

    return [h1_ok, neg_Q]

CONDITION_LABELS = [
    "H_1: f is continuous on the interval from a to b",
    "not Q: inf D^+f(x) > (f(b)-f(a))/(b-a) or sup D^+f(x) < (f(b)-f(a))/(b-a)"
]
N_HYP = 1
NEG_Q_INDEX = 1