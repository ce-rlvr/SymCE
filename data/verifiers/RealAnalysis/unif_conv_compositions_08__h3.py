import sympy
from sympy import Symbol, S, Interval, oo, limit, Abs, simplify
from sympy.calculus.util import maximum, minimum

# Top-level setup: named object bindings that the witness expression may reference
x = Symbol('x', real=True)
n = Symbol('n', integer=True, positive=True)
R = S.Reals

def check_uniform_convergence(expr_n, expr, x_sym, n_sym, domain):
    try:
        diff = simplify(expr_n - expr)
    except Exception:
        diff = expr_n - expr
        
    if x_sym not in diff.free_symbols:
        try:
            return limit(Abs(diff), n_sym, oo) == 0
        except Exception:
            return False
            
    # 1. Try limits at boundaries and critical points
    try:
        from sympy import diff as sympy_diff, solve
        pts_to_check = []
        
        if hasattr(domain, 'start') and hasattr(domain, 'end'):
            pts_to_check.extend([domain.start, domain.end])
            
        if domain == S.Reals:
            pts_to_check.extend([oo, -oo])
            
        try:
            deriv = sympy_diff(diff, x_sym)
            crit_pts = solve(deriv, x_sym)
            if isinstance(crit_pts, list):
                pts_to_check.extend(crit_pts)
        except Exception:
            pass
            
        for pt in pts_to_check:
            try:
                if hasattr(pt, 'free_symbols') and x_sym in pt.free_symbols:
                    continue
                val = limit(diff, x_sym, pt)
                if val == oo or val == -oo:
                    return False
                
                lim_val = limit(Abs(val), n_sym, oo)
                if lim_val == oo:
                    return False
                try:
                    if bool(lim_val > 0):
                        return False
                except TypeError:
                    pass
            except Exception:
                pass
    except Exception:
        pass

    # 2. Try maximum/minimum
    try:
        max_val = maximum(diff, x_sym, domain)
        min_val = minimum(diff, x_sym, domain)
        
        if max_val == oo or min_val == -oo:
            return False
            
        lim_max = limit(max_val, n_sym, oo)
        lim_min = limit(min_val, n_sym, oo)
        
        if lim_max == 0 and lim_min == 0:
            return True
    except Exception:
        pass
        
    return False

def conditions(witness) -> list[bool]:
    """
    witness is expected to be a tuple: (domain, f_n, f, g)
    where:
      - domain is a sympy Set (e.g., R or Interval(0, 1))
      - f_n is a sympy expression in x and n (or a callable)
      - f is a sympy expression in x (or a callable)
      - g is a sympy expression in x (or a callable)
    """
    try:
        domain, f_n, f, g = witness
    except Exception:
        return [False, False, False]
        
    # H1: S is a non-empty set
    try:
        from sympy import Set
        h1 = isinstance(domain, Set) and (domain.is_empty is not True)
    except Exception:
        h1 = False
        
    try:
        f_n_expr = f_n(x, n) if callable(f_n) else f_n
        f_expr = f(x) if callable(f) else f
    except Exception:
        return [bool(h1), False, False]
        
    # H2: f_n converges uniformly to f on S
    try:
        h2 = check_uniform_convergence(f_n_expr, f_expr, x, n, domain)
    except Exception:
        h2 = False
        
    # neg_Q: g(f_n) does NOT converge uniformly to g(f) on S
    try:
        g_fn = g(f_n_expr) if callable(g) else g.subs(x, f_n_expr)
        g_f = g(f_expr) if callable(g) else g.subs(x, f_expr)
        
        neg_q = not check_uniform_convergence(g_fn, g_f, x, n, domain)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: S is a non-empty set",
    "H_2: {f_n} converges uniformly to f on S",
    "¬Q: {g ∘ f_n} does not converge uniformly to g ∘ f on S"
]

N_HYP = 2
NEG_Q_INDEX = 2