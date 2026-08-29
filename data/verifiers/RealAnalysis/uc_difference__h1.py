import sympy as sp

# Top-level setup
x = sp.Symbol('x', real=True)

def is_uniformly_continuous(expr, domain):
    try:
        # Check continuity on the domain
        try:
            cd = sp.calculus.util.continuous_domain(expr, x, domain)
            if not domain.is_subset(cd):
                return False
        except Exception:
            return False
            
        # Check limits at finite open boundaries to rule out vertical asymptotes or oscillation
        if domain.is_Interval:
            if domain.start.is_finite and domain.left_open:
                lim = sp.limit(expr, x, domain.start, dir='+')
                if lim in [sp.oo, -sp.oo, sp.zoo] or type(lim).__name__ == 'AccumBounds':
                    return False
            if domain.end.is_finite and domain.right_open:
                lim = sp.limit(expr, x, domain.end, dir='-')
                if lim in [sp.oo, -sp.oo, sp.zoo] or type(lim).__name__ == 'AccumBounds':
                    return False
                    
        # If domain is bounded and closed, continuous implies uniformly continuous
        if domain.is_Interval and not domain.left_open and not domain.right_open:
            if domain.start.is_finite and domain.end.is_finite:
                return True
                
        # Polynomial check: degree must be <= 1 for unbounded domains
        if expr.is_polynomial(x):
            deg = sp.degree(expr, x)
            if not domain.is_bounded and deg > 1:
                return False
            return True
            
        # Derivative check
        df = sp.diff(expr, x)
        
        # If domain is unbounded, check limits of the derivative
        if domain.is_Interval:
            if domain.end == sp.oo:
                lim = sp.limit(df, x, sp.oo)
                if lim in [sp.oo, -sp.oo, sp.zoo] or type(lim).__name__ == 'AccumBounds':
                    return False
            if domain.start == -sp.oo:
                lim = sp.limit(df, x, -sp.oo)
                if lim in [sp.oo, -sp.oo, sp.zoo] or type(lim).__name__ == 'AccumBounds':
                    return False
                    
        # Try to compute the range of the derivative to see if it's bounded
        try:
            df_range = sp.calculus.util.function_range(df, x, domain)
            if df_range.sup.is_finite and df_range.inf.is_finite:
                return True
        except Exception:
            pass
            
        # Default to True as a fallback
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            f = witness.get('f')
            g = witness.get('g')
            domain = witness.get('domain', sp.S.Reals)
        elif isinstance(witness, tuple):
            if len(witness) == 3:
                f, g, domain = witness
            elif len(witness) == 2:
                f, g = witness
                domain = sp.S.Reals
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        if isinstance(domain, tuple) and len(domain) == 2:
            domain = sp.Interval(domain[0], domain[1])
            
        if callable(f):
            f_expr = f(x)
        else:
            f_expr = f
            
        if callable(g):
            g_expr = g(x)
        else:
            g_expr = g
            
        h_expr = f_expr - g_expr
        
        h1 = is_uniformly_continuous(f_expr, domain)
        h2 = is_uniformly_continuous(g_expr, domain)
        q = is_uniformly_continuous(h_expr, domain)
        
        return [bool(h1), bool(h2), not bool(q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: f is uniformly continuous on X",
    "H_2: g is uniformly continuous on X",
    "¬Q: h(x) = f(x) - g(x) is not uniformly continuous on X"
]

N_HYP = 2
NEG_Q_INDEX = 2