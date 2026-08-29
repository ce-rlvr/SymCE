import sympy
from sympy import Symbol, Interval, oo, Limit, diff, Abs, S
from sympy.calculus.util import continuous_domain, function_range

# Top-level setup
x = Symbol('x', real=True)

def is_uniformly_continuous(f, domain, var):
    if not hasattr(domain, 'is_Interval') or not domain.is_Interval:
        return False

    try:
        cd = continuous_domain(f, var, domain)
        if not domain.is_subset(cd):
            return False
    except Exception:
        return False

    # A continuous function on a closed bounded interval is uniformly continuous
    if not domain.left_open and not domain.right_open and domain.measure < oo:
        return True

    # A function with a bounded derivative on an interval is uniformly continuous
    df = diff(f, var)
    try:
        frange = function_range(df, var, domain)
        if frange.inf > -oo and frange.sup < oo:
            return True
    except Exception:
        pass
        
    # A continuous function with finite limits at the boundaries of its interval domain is uniformly continuous
    try:
        left_lim = Limit(f, var, domain.start, dir='+').doit()
        right_lim = Limit(f, var, domain.end, dir='-').doit()
        if left_lim.is_number and left_lim.is_finite and right_lim.is_number and right_lim.is_finite:
            return True
    except Exception:
        pass

    return False

def is_bounded_away_from_zero(f, domain, var):
    try:
        frange = function_range(Abs(f), var, domain)
        if frange.inf.is_number and frange.inf > 0:
            return True
    except Exception:
        pass
    return False

def is_NOT_uniformly_continuous(f, domain, var):
    if not hasattr(domain, 'is_Interval') or not domain.is_Interval:
        pass
        
    # If it's not even continuous, it's not uniformly continuous
    try:
        cd = continuous_domain(f, var, domain)
        if not domain.is_subset(cd):
            return True
    except Exception:
        pass

    # Infinite limits at finite boundaries imply vertical asymptotes (not uniformly continuous)
    try:
        if domain.start.is_finite:
            left_lim = Limit(f, var, domain.start, dir='+').doit()
            if left_lim.is_infinite:
                return True
        if domain.end.is_finite:
            right_lim = Limit(f, var, domain.end, dir='-').doit()
            if right_lim.is_infinite:
                return True
    except Exception:
        pass

    # Superlinear growth at infinity implies not uniformly continuous
    try:
        if domain.end == oo:
            lim = Limit(f/var, var, oo).doit()
            if lim.is_infinite:
                return True
        if domain.start == -oo:
            lim = Limit(f/var, var, -oo).doit()
            if lim.is_infinite:
                return True
    except Exception:
        pass

    return False

def conditions(witness):
    """
    witness: tuple of (f_expr, domain)
    Example: (x**2, Interval(0, oo))
    """
    try:
        f_expr, domain = witness
        if domain == S.Reals:
            domain = Interval(-oo, oo)
            
        symbols = f_expr.free_symbols
        if len(symbols) == 1:
            var = list(symbols)[0]
        elif len(symbols) == 0:
            var = x
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    try:
        h1 = bool(is_uniformly_continuous(f_expr, domain, var))
    except Exception:
        h1 = False
        
    try:
        h2 = bool(is_bounded_away_from_zero(f_expr, domain, var))
    except Exception:
        h2 = False
        
    try:
        neg_q = bool(is_NOT_uniformly_continuous(1/f_expr, domain, var))
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is uniformly continuous on X",
    "H_2: There exists a constant c > 0 such that |f(x)| >= c for all x in X",
    "¬Q: g(x) = 1/f(x) is not uniformly continuous on X"
]

N_HYP = 2
NEG_Q_INDEX = 2