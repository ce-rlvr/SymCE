import sympy as sp
from sympy import Symbol, Abs, S, oo, Interval, Union, Intersection, FiniteSet, sin, cos, exp, log, sqrt, pi

# Top-level setup for witness expressions
x = Symbol('x', real=True)
y = Symbol('y', real=True)
z = Symbol('z', real=True)

def check_is_oo(val):
    if val == oo:
        return True
    if hasattr(val, 'min') and hasattr(val, 'max'):
        if val.min == -oo or val.max == oo:
            return True
    return False

def is_bounded(expr, domain, sym):
    try:
        rng = sp.calculus.util.function_range(expr, sym, domain)
        if rng.inf > -oo and rng.sup < oo:
            return True
    except Exception:
        pass
    try:
        max_val = sp.maximum(Abs(expr), sym, domain)
        if max_val < oo:
            return True
    except Exception:
        pass
    return False

def is_lipschitz(expr, domain, sym):
    try:
        deriv = sp.diff(expr, sym)
        max_deriv = sp.maximum(Abs(deriv), sym, domain)
        if max_deriv < oo:
            return True
    except Exception:
        pass
    try:
        deriv = sp.diff(expr, sym)
        rng = sp.calculus.util.function_range(Abs(deriv), sym, domain)
        if rng.sup < oo:
            return True
    except Exception:
        pass
    return False

def is_bounded_away_from_zero(expr, domain, sym):
    try:
        min_val = sp.minimum(Abs(expr), sym, domain)
        if min_val > 0:
            return True
    except Exception:
        pass
    try:
        rng = sp.calculus.util.function_range(Abs(expr), sym, domain)
        if rng.inf > 0:
            return True
    except Exception:
        pass
    return False

def is_not_lipschitz(expr, domain, sym):
    try:
        deriv = sp.diff(expr, sym)
        max_deriv = sp.maximum(Abs(deriv), sym, domain)
        if check_is_oo(max_deriv):
            return True
    except Exception:
        pass
        
    try:
        deriv = sp.diff(expr, sym)
        rng = sp.calculus.util.function_range(Abs(deriv), sym, domain)
        if check_is_oo(rng.sup):
            return True
    except Exception:
        pass
    
    try:
        deriv = sp.diff(expr, sym)
        if isinstance(domain, sp.Union):
            intervals = domain.args
        elif isinstance(domain, sp.Interval):
            intervals = [domain]
        else:
            intervals = []
            
        for interval in intervals:
            if isinstance(interval, sp.Interval):
                start = interval.start
                end = interval.end
                if start != -oo:
                    lim = sp.limit(Abs(deriv), sym, start, dir='+')
                    if check_is_oo(lim):
                        return True
                else:
                    lim = sp.limit(Abs(deriv), sym, -oo)
                    if check_is_oo(lim):
                        return True
                
                if end != oo:
                    lim = sp.limit(Abs(deriv), sym, end, dir='-')
                    if check_is_oo(lim):
                        return True
                else:
                    lim = sp.limit(Abs(deriv), sym, oo)
                    if check_is_oo(lim):
                        return True
    except Exception:
        pass
        
    try:
        deriv = sp.diff(expr, sym)
        sing = sp.calculus.singularities(deriv, sym)
        if isinstance(sing, sp.Set):
            sing_in_domain = sing.intersect(domain)
            for pt in sing_in_domain:
                lim = sp.limit(Abs(deriv), sym, pt)
                if check_is_oo(lim):
                    return True
    except Exception:
        pass

    return False

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 3:
            domain, f, g = witness
        elif len(witness) == 2:
            f, g = witness
            domain = sp.S.Reals
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]
        
    try:
        f_expr = sp.sympify(f)
        g_expr = sp.sympify(g)
        symbols = f_expr.free_symbols | g_expr.free_symbols
        sym = list(symbols)[0] if symbols else x
    except Exception:
        return [False, False, False, False]

    # H1: X is a metric space
    try:
        h1 = isinstance(domain, sp.Set)
    except Exception:
        h1 = False
        
    # H2: f is bounded and globally Lipschitz continuous
    try:
        h2 = is_bounded(f_expr, domain, sym) and is_lipschitz(f_expr, domain, sym)
    except Exception:
        h2 = False
        
    # H3: There exists a constant c > 0 such that |g(x)| >= c for all x in X
    try:
        h3 = is_bounded_away_from_zero(g_expr, domain, sym)
    except Exception:
        h3 = False
        
    # neg_Q: The quotient function f/g is NOT globally Lipschitz continuous on X
    try:
        neg_q = is_not_lipschitz(f_expr / g_expr, domain, sym)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: X is a metric space",
    "H_2: f is bounded and globally Lipschitz continuous",
    "H_3: There exists a constant c > 0 such that |g(x)| >= c for all x in X",
    "¬Q: The quotient function f/g is not globally Lipschitz continuous on X"
]

N_HYP = 3
NEG_Q_INDEX = 3