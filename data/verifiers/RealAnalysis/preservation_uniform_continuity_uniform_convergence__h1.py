import sympy as sp
from sympy.calculus.util import maximum
from sympy.calculus.singularities import singularities
import math

# Top-level setup
x, n = sp.symbols('x n', real=True)
Interval = sp.Interval
oo = sp.oo

CONDITION_LABELS = [
    "H_1: Each function f_n is uniformly continuous on S",
    "H_2: The sequence (f_n) converges uniformly to f on S",
    "¬Q: The limit function f is NOT uniformly continuous on S"
]

N_HYP = 2
NEG_Q_INDEX = 2

def check_uniform_continuity(g, x_sym, S):
    # 1. Closed and bounded
    try:
        if S.is_closed and S.is_bounded:
            sings = singularities(g, x_sym)
            if sings.intersect(S).is_empty:
                return True
            else:
                return False
    except Exception:
        pass

    # 2. Bounded derivative
    try:
        g_prime = sp.diff(g, x_sym)
        max_deriv = maximum(sp.Abs(g_prime), x_sym, S)
        if max_deriv < sp.oo:
            return True
    except Exception:
        pass

    # 3. Continuous and finite limits at infinity
    try:
        sings = singularities(g, x_sym)
        is_cont = sings.intersect(S).is_empty
        if is_cont:
            if S.sup == sp.oo and S.inf == -sp.oo:
                lim_inf = sp.limit(g, x_sym, sp.oo)
                lim_minf = sp.limit(g, x_sym, -sp.oo)
                if lim_inf.is_real and lim_minf.is_real:
                    return True
            elif S.sup == sp.oo:
                lim_inf = sp.limit(g, x_sym, sp.oo)
                if lim_inf.is_real:
                    return True
            elif S.inf == -sp.oo:
                lim_minf = sp.limit(g, x_sym, -sp.oo)
                if lim_minf.is_real:
                    return True
    except Exception:
        pass

    # 4. Derivative goes to 0 at infinity, AND finite limit at finite endpoints
    try:
        g_prime = sp.diff(g, x_sym)
        sings = singularities(g, x_sym)
        if sings.intersect(S).is_empty:
            endpoints_ok = True
            if S.inf != -sp.oo:
                lim_start = sp.limit(g, x_sym, S.inf, dir='+')
                if not lim_start.is_real:
                    endpoints_ok = False
            if S.sup != sp.oo:
                lim_end = sp.limit(g, x_sym, S.sup, dir='-')
                if not lim_end.is_real:
                    endpoints_ok = False
            
            if endpoints_ok:
                if S.sup == sp.oo and S.inf != -sp.oo:
                    if sp.limit(g_prime, x_sym, sp.oo) == 0:
                        return True
                elif S.inf == -sp.oo and S.sup != sp.oo:
                    if sp.limit(g_prime, x_sym, -sp.oo) == 0:
                        return True
                elif S.inf == -sp.oo and S.sup == sp.oo:
                    if sp.limit(g_prime, x_sym, sp.oo) == 0 and sp.limit(g_prime, x_sym, -sp.oo) == 0:
                        return True
    except Exception:
        pass

    # 5. Polynomials
    try:
        poly = sp.Poly(g, x_sym)
        if poly.degree() > 1 and not S.is_bounded:
            return False
        if poly.degree() <= 1:
            return True
    except Exception:
        pass

    # 6. Necessary condition for unbounded domains
    try:
        if not S.is_bounded:
            diff = sp.simplify(g.subs(x_sym, x_sym + 1/x_sym) - g)
            lim = sp.limit(diff, x_sym, sp.oo)
            if lim != 0:
                return False
    except Exception:
        pass

    # 7. Check for vertical asymptotes in bounded open intervals
    try:
        if S.is_bounded and not S.is_closed:
            lim_start = sp.limit(g, x_sym, S.inf, dir='+')
            lim_end = sp.limit(g, x_sym, S.sup, dir='-')
            if not lim_start.is_real or not lim_end.is_real:
                return False
            sings = singularities(g, x_sym)
            if sings.intersect(S).is_empty:
                return True
    except Exception:
        pass

    # Fallback heuristic: evaluate derivative on a grid
    try:
        g_prime = sp.diff(g, x_sym)
        f_lamb = sp.lambdify(x_sym, sp.Abs(g_prime), 'math')
        if S.is_bounded:
            left = float(S.inf) + 1e-5
            right = float(S.sup) - 1e-5
            grid = [left + (right - left) * i / 100.0 for i in range(101)]
        else:
            left = float(S.inf) if S.inf != -sp.oo else -1000.0
            right = float(S.sup) if S.sup != sp.oo else 1000.0
            grid = [left + (right - left) * i / 100.0 for i in range(101)]
        
        max_val = 0
        for val in grid:
            try:
                v = f_lamb(val)
                if v > max_val:
                    max_val = v
            except Exception:
                pass
        if max_val < 1000:
            return True
    except Exception:
        pass

    return False

def check_fn_uniformly_continuous(f_n, x_sym, n_sym, S):
    for n_val in [1, 2, 3, 10]:
        f_n_val = f_n.subs(n_sym, n_val)
        if not check_uniform_continuity(f_n_val, x_sym, S):
            return False
    return True

def check_uniform_convergence(f_n, f, x_sym, n_sym, S):
    diff = sp.Abs(f_n - f)
    try:
        max_diff = maximum(diff, x_sym, S)
        lim = sp.limit(max_diff, n_sym, sp.oo)
        if lim == 0:
            return True
        if lim > 0 or lim == sp.oo:
            return False
    except Exception:
        pass

    # Fallback: evaluate on a grid
    try:
        if S.is_bounded:
            left = float(S.inf)
            right = float(S.sup)
            grid = [left + (right - left) * i / 100.0 for i in range(1, 100)]
            grid += [left + 1e-3, left + 1e-4, left + 1e-5]
            grid += [right - 1e-3, right - 1e-4, right - 1e-5]
        else:
            left = float(S.inf) if S.inf != -sp.oo else -1000.0
            right = float(S.sup) if S.sup != sp.oo else 1000.0
            grid = [left + (right - left) * i / 100.0 for i in range(1, 100)]
            if S.sup == sp.oo:
                grid += [10**k for k in range(3, 7)]
            if S.inf == -sp.oo:
                grid += [-10**k for k in range(3, 7)]
                
        max_vals = []
        for n_val in [100, 1000, 10000]:
            diff_n = diff.subs(n_sym, n_val)
            f_lamb = sp.lambdify(x_sym, diff_n, 'math')
            vals = []
            for val in grid:
                try:
                    vals.append(abs(f_lamb(val)))
                except Exception:
                    pass
            if vals:
                max_vals.append(max(vals))
        if len(max_vals) == 3:
            if max_vals[-1] < 1e-2:
                return True
            return False
    except Exception:
        pass
    
    return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            f_n_val = witness.get('f_n', sp.Integer(0))
            f_val = witness.get('f', sp.Integer(0))
            S_val = witness.get('S', sp.Interval(-sp.oo, sp.oo))
        else:
            f_n_val, f_val, S_val = witness
            
        if isinstance(f_n_val, str):
            f_n_expr = sp.sympify(f_n_val, locals={'x': x, 'n': n})
        else:
            f_n_expr = f_n_val
            
        if isinstance(f_val, str):
            f_expr = sp.sympify(f_val, locals={'x': x})
        else:
            f_expr = f_val
            
        if isinstance(S_val, str):
            S_obj = sp.sympify(S_val)
            if isinstance(S_obj, list) and len(S_obj) == 2:
                S_expr = sp.Interval(S_obj[0], S_obj[1])
            elif isinstance(S_obj, tuple) and len(S_obj) == 2:
                S_expr = sp.Interval(S_obj[0], S_obj[1])
            else:
                S_expr = S_obj
        elif isinstance(S_val, (list, tuple)) and len(S_val) == 2:
            S_expr = sp.Interval(S_val[0], S_val[1])
        else:
            S_expr = S_val
            
        free_symbols = set()
        if hasattr(f_n_expr, 'free_symbols'):
            free_symbols |= f_n_expr.free_symbols
        if hasattr(f_expr, 'free_symbols'):
            free_symbols |= f_expr.free_symbols
            
        x_sym = x
        n_sym = n
        for sym in free_symbols:
            if sym.name == 'x':
                x_sym = sym
            elif sym.name == 'n':
                n_sym = sym
                
        try:
            h1 = check_fn_uniformly_continuous(f_n_expr, x_sym, n_sym, S_expr)
        except Exception:
            h1 = False
            
        try:
            h2 = check_uniform_convergence(f_n_expr, f_expr, x_sym, n_sym, S_expr)
        except Exception:
            h2 = False
            
        try:
            q = check_uniform_continuity(f_expr, x_sym, S_expr)
            neg_q = not q
        except Exception:
            neg_q = False
            
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]