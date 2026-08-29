import sympy
from sympy import limit, Abs, degree, diff, oo, nan

# Top-level setup
x, y, z = sympy.symbols('x y z')

def is_uniformly_continuous(expr, domain, var):
    if domain == sympy.S.Reals:
        domain = sympy.Interval(-oo, oo)

    if not isinstance(domain, sympy.Interval):
        return None

    try:
        from sympy.calculus.singularities import singularities
        sings = singularities(expr, var)
        if isinstance(sings, sympy.Set):
            intersection = sings.intersect(domain)
            if intersection.is_empty is False:
                return False
    except Exception:
        pass

    try:
        if domain.left_open and domain.inf != -oo:
            L = limit(expr, var, domain.inf, dir='+')
            if L in (oo, -oo, nan) or L.has(sympy.AccumBounds) or L.has(sympy.oo) or L.has(sympy.nan):
                return False
        if domain.right_open and domain.sup != oo:
            R = limit(expr, var, domain.sup, dir='-')
            if R in (oo, -oo, nan) or R.has(sympy.AccumBounds) or R.has(sympy.oo) or R.has(sympy.nan):
                return False
    except Exception:
        pass

    if domain.measure < oo:
        return True
            
    if domain.measure == oo:
        if expr.is_polynomial(var):
            deg = degree(expr, var)
            if deg <= 1:
                return True
            else:
                return False
                
        d_expr = diff(expr, var)
        try:
            if domain.sup == oo:
                lim_inf = limit(d_expr, var, oo)
                if Abs(lim_inf) == oo:
                    return False
            if domain.inf == -oo:
                lim_neg_inf = limit(d_expr, var, -oo)
                if Abs(lim_neg_inf) == oo:
                    return False
        except Exception:
            pass
            
        if d_expr.is_constant():
            return True
            
        try:
            from sympy.calculus.util import maximum
            max_val = maximum(Abs(d_expr), var, domain)
            if max_val < oo:
                return True
        except Exception:
            pass
            
        if expr == sympy.sqrt(var) and domain == sympy.Interval(0, oo):
            return True
            
    return None

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            f = witness['f']
            g = witness['g']
            X = witness['X']
            Y = witness['Y']
            var = witness.get('var', sympy.Symbol('x'))
        else:
            f, g, X, Y = witness
            var = sympy.Symbol('x')
            free_vars = f.free_symbols | g.free_symbols
            if len(free_vars) == 1:
                var = list(free_vars)[0]
    except Exception:
        return [False, False, False]
        
    # H1: X, Y, and Z are metric spaces
    try:
        h1 = isinstance(X, sympy.Set) and isinstance(Y, sympy.Set)
    except Exception:
        h1 = False
        
    # H2: f: X -> Y is uniformly continuous
    try:
        maps_to_Y = True
        if Y != sympy.S.Reals and Y != sympy.Interval(-oo, oo):
            try:
                from sympy.calculus.util import function_range
                frange = function_range(f, var, X)
                maps_to_Y = frange.is_subset(Y)
            except Exception:
                pass
        
        uc_f = is_uniformly_continuous(f, X, var)
        h2 = maps_to_Y and (uc_f is True)
    except Exception:
        h2 = False
        
    # Negated Conclusion: g o f: X -> Z is not uniformly continuous
    try:
        g_vars = g.free_symbols
        if len(g_vars) == 1:
            g_var = list(g_vars)[0]
            g_of_f = g.subs(g_var, f)
        else:
            g_of_f = g.subs(var, f)
            
        uc_g_of_f = is_uniformly_continuous(g_of_f, X, var)
        neg_q = (uc_g_of_f is False)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: X, Y, and Z are metric spaces",
    "H_2: f: X -> Y is uniformly continuous",
    "¬Q: g o f: X -> Z is not uniformly continuous"
]

N_HYP = 2
NEG_Q_INDEX = 2