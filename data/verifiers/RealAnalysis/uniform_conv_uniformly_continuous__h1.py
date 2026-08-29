import sympy as sp
from sympy.abc import x, n
from sympy.calculus.util import continuous_domain, maximum

# Top-level setup
# The witness is expected to be a dictionary with keys 'domain', 'f_n', and 'f'.
# Expressions should be written in terms of the symbolic variables x and n.

def is_uniformly_continuous(expr, domain, var):
    """Sound but incomplete check for uniform continuity."""
    try:
        is_compact = False
        if isinstance(domain, sp.Interval):
            if not domain.left_open and not domain.right_open and domain.measure < sp.oo:
                is_compact = True
        elif isinstance(domain, sp.FiniteSet):
            is_compact = True
            
        if is_compact:
            if continuous_domain(expr, var, domain) == domain:
                return True
                
        dexpr = sp.diff(expr, var)
        if dexpr == 0 or not dexpr.has(var):
            return True
            
        max_d = maximum(sp.Abs(dexpr), var, domain)
        if max_d < sp.oo:
            return True
            
        if isinstance(domain, sp.Interval) and domain.sup == sp.oo:
            if continuous_domain(expr, var, domain) == domain:
                lim = sp.limit(dexpr, var, sp.oo)
                if lim != sp.oo and lim != -sp.oo and not lim.has(sp.oo) and not lim.has(-sp.oo):
                    if lim.is_number:
                        return True
    except Exception:
        pass
    return False

def is_NOT_uniformly_continuous(expr, domain, var):
    """Sound but incomplete check for NOT uniformly continuous."""
    try:
        if isinstance(domain, sp.Interval):
            if domain.left_open and domain.inf != -sp.oo:
                lim = sp.limit(expr, var, domain.inf, dir='+')
                if lim in [sp.oo, -sp.oo]:
                    return True
            if domain.right_open and domain.sup != sp.oo:
                lim = sp.limit(expr, var, domain.sup, dir='-')
                if lim in [sp.oo, -sp.oo]:
                    return True
                    
        dexpr = sp.diff(expr, var)
        if isinstance(domain, sp.Interval):
            if domain.sup == sp.oo:
                lim = sp.limit(dexpr, var, sp.oo)
                if lim in [sp.oo, -sp.oo]:
                    return True
            if domain.inf == -sp.oo:
                lim = sp.limit(dexpr, var, -sp.oo)
                if lim in [sp.oo, -sp.oo]:
                    return True
                    
        try:
            singularities = sp.singularities(expr, var)
            if not sp.Intersection(singularities, domain).is_empty:
                return True
        except Exception:
            pass
            
        if expr.is_polynomial(var) and domain.measure == sp.oo:
            if sp.degree(expr, var) >= 2:
                return True
                
    except Exception:
        pass
    return False

def is_uniformly_convergent(f_n, f, domain, var, n_var):
    """Sound but incomplete check for uniform convergence."""
    try:
        diff_expr = sp.simplify(f_n - f)
        if diff_expr == 0:
            return True
            
        if not diff_expr.has(var):
            lim = sp.limit(diff_expr, n_var, sp.oo)
            if lim == 0:
                return True
                
        try:
            sup = maximum(sp.Abs(diff_expr), var, domain)
            if sup.has(n_var):
                lim = sp.limit(sup, n_var, sp.oo)
                if lim == 0:
                    return True
            elif sup == 0:
                return True
        except Exception:
            pass
            
        try:
            d_diff = sp.diff(diff_expr, var)
            crit_points = sp.solve(d_diff, var)
            
            candidates = []
            
            if isinstance(domain, sp.Interval):
                if domain.inf != -sp.oo:
                    candidates.append(sp.Abs(diff_expr).subs(var, domain.inf))
                else:
                    candidates.append(sp.limit(sp.Abs(diff_expr), var, -sp.oo))
                    
                if domain.sup != sp.oo:
                    candidates.append(sp.Abs(diff_expr).subs(var, domain.sup))
                else:
                    candidates.append(sp.limit(sp.Abs(diff_expr), var, sp.oo))
            elif isinstance(domain, sp.FiniteSet):
                for pt in domain:
                    candidates.append(sp.Abs(diff_expr).subs(var, pt))
                    
            for cp in crit_points:
                if cp.is_real or cp.is_real is None:
                    candidates.append(sp.Abs(diff_expr).subs(var, cp))
                    
            all_zero = True
            for cand in candidates:
                lim = sp.limit(cand, n_var, sp.oo)
                if lim != 0:
                    all_zero = False
                    break
            if all_zero and len(candidates) > 0:
                return True
        except Exception:
            pass
            
    except Exception:
        pass
    return False

def conditions(witness) -> list[bool]:
    try:
        domain = witness.get('domain')
        if domain == sp.S.Reals:
            domain = sp.Interval(-sp.oo, sp.oo)
        f_n_expr = sp.sympify(witness.get('f_n'))
        f_expr = sp.sympify(witness.get('f'))
    except Exception:
        return [False, False, False, False]
        
    # H_1: {f_n} is a sequence of functions from S to R
    try:
        h1 = isinstance(domain, sp.Set) and f_n_expr is not None and f_expr is not None
    except Exception:
        h1 = False
        
    # H_2: Each f_n is uniformly continuous on S
    try:
        h2 = True
        for n_val in [1, 2, 3]:
            fn_sub = f_n_expr.subs(n, n_val)
            if not is_uniformly_continuous(fn_sub, domain, x):
                h2 = False
                break
    except Exception:
        h2 = False
        
    # H_3: The sequence {f_n} converges uniformly to a function f on S
    try:
        h3 = is_uniformly_convergent(f_n_expr, f_expr, domain, x, n)
    except Exception:
        h3 = False
        
    # ¬Q: The limit function f is NOT uniformly continuous on S
    try:
        neg_q = is_NOT_uniformly_continuous(f_expr, domain, x)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: {f_n} is a sequence of functions from S to R",
    "H_2: Each f_n is uniformly continuous on S",
    "H_3: The sequence {f_n} converges uniformly to a function f on S",
    "¬Q: The limit function f is NOT uniformly continuous on S"
]

N_HYP = 3
NEG_Q_INDEX = 3