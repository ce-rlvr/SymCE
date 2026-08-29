import sympy
from sympy import Symbol, Piecewise, Interval, oo, limit, solveset, EmptySet

x = Symbol('x', real=True)
n = Symbol('n', integer=True, positive=True)

def check_no_root_numerically(func, a, b):
    grid = [a + (b - a) * i / 1000.0 for i in range(1001)]
    for i in range(1000):
        x1, x2 = grid[i], grid[i+1]
        try:
            v1, v2 = float(func(x1)), float(func(x2))
        except Exception:
            continue
        
        if v1 == 0 and a < x1 < b:
            return False
        if v2 == 0 and a < x2 < b:
            return False
            
        if v1 * v2 < 0:
            for _ in range(20):
                xm = (x1 + x2) / 2.0
                try:
                    vm = float(func(xm))
                except Exception:
                    break
                if vm == 0:
                    return False
                if v1 * vm <= 0:
                    x2, v2 = xm, vm
                else:
                    x1, v1 = xm, vm
            if min(abs(v1), abs(v2)) < 1e-2:
                return False
    return True

def conditions(witness) -> list[bool]:
    try:
        f_n, f, a, b = witness
    except Exception:
        return [False, False, False]
        
    is_sympy = hasattr(f_n, 'subs')
    
    h1_ok = False
    try:
        pts = [a, b]
        for i in range(1, 20):
            pts.append(a + (b - a) * (i / 20.0))
            
        h1_ok = True
        for pt in pts:
            if is_sympy:
                f_val = float(f.subs(x, pt))
                fn_pt = f_n.subs(x, pt)
                
                lim_val = None
                try:
                    lim_val = float(limit(fn_pt, n, oo))
                except Exception:
                    pass
                
                if lim_val is not None and abs(lim_val - f_val) <= 1e-3:
                    continue
                
                val_large = float(fn_pt.subs(n, 1000000))
                if abs(val_large - f_val) <= 1e-3:
                    continue
                
                h1_ok = False
                break
            else:
                f_val = float(f(pt))
                val_large = float(f_n(1000000, pt))
                if abs(val_large - f_val) > 1e-3:
                    h1_ok = False
                    break
    except Exception:
        h1_ok = False

    h2_ok = False
    try:
        if is_sympy:
            fa = float(f.subs(x, a))
            fb = float(f.subs(x, b))
        else:
            fa = float(f(a))
            fb = float(f(b))
        h2_ok = (fa * fb < 0)
    except Exception:
        h2_ok = False

    neg_q_ok = False
    try:
        all_no_root = True
        for nv in [10, 50, 100]:
            if is_sympy:
                fn_sub = f_n.subs(n, nv)
                try:
                    roots = solveset(fn_sub, x, domain=Interval.open(a, b))
                except Exception:
                    roots = None
                
                if roots is not None:
                    if roots == EmptySet or (hasattr(roots, 'is_empty') and roots.is_empty is True):
                        continue
                    elif hasattr(roots, 'is_empty') and roots.is_empty is False:
                        all_no_root = False
                        break
                
                def func_sympy(xv, fn_sub=fn_sub):
                    return fn_sub.subs(x, xv)
                if check_no_root_numerically(func_sympy, a, b):
                    continue
                all_no_root = False
                break
            else:
                def func_py(xv, nv=nv):
                    return f_n(nv, xv)
                if check_no_root_numerically(func_py, a, b):
                    continue
                all_no_root = False
                break
        neg_q_ok = all_no_root
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    'H_1: The sequence f_n converges pointwise to f on the interval',
    'H_2: f(a) * f(b) < 0',
    'not Q: For all N, there exists n >= N such that f_n has no root'
]

N_HYP = 2
NEG_Q_INDEX = 2