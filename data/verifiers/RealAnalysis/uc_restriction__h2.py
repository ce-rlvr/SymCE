import sympy
from sympy import Set, Symbol, Interval, oo, S, limit
from sympy.calculus.util import continuous_domain, function_range, AccumBounds
from sympy.abc import x, y, z

# Top-level setup
# Standard symbols for real analysis expressions
# (No group theory or linear algebra objects needed for this domain)

def is_uniformly_continuous(f_expr, A_set, Y_set, sym):
    # If A is a subset of integers, any function is uniformly continuous on it
    try:
        if A_set.is_subset(S.Integers) == True:
            return True
    except Exception:
        pass

    # Check if f maps A to Y
    try:
        rng = function_range(f_expr, sym, A_set)
        if not rng.is_subset(Y_set):
            return False
    except Exception:
        pass

    # 1. Check continuity on A
    try:
        dom = continuous_domain(f_expr, sym, S.Reals)
        if not A_set.is_subset(dom):
            return False
    except Exception:
        pass

    # 2. Check finite boundaries
    try:
        for pt in A_set.boundary:
            if pt in [oo, -oo]:
                continue
            
            if not A_set.intersect(Interval.Lopen(pt, pt+1)).is_empty:
                l = limit(f_expr, sym, pt, dir='+')
            elif not A_set.intersect(Interval.Ropen(pt-1, pt)).is_empty:
                l = limit(f_expr, sym, pt, dir='-')
            else:
                l = limit(f_expr, sym, pt)
            
            if isinstance(l, AccumBounds):
                return False
            if getattr(l, 'is_infinite', False):
                return False
            if getattr(l, 'is_real', None) is False:
                return False
    except Exception:
        pass

    # 3. Check unbounded A
    try:
        if not A_set.is_bounded:
            df = f_expr.diff(sym)
            
            def check_limit_at_inf(lim_val):
                if isinstance(lim_val, AccumBounds):
                    if getattr(lim_val.min, 'is_infinite', False) or getattr(lim_val.max, 'is_infinite', False):
                        return False
                elif getattr(lim_val, 'is_infinite', False):
                    return False
                elif getattr(lim_val, 'is_real', None) is False:
                    return False
                return True

            if getattr(A_set, 'sup', None) == oo:
                l_df = limit(df, sym, oo)
                if not check_limit_at_inf(l_df):
                    return False
                    
            if getattr(A_set, 'inf', None) == -oo:
                l_df = limit(df, sym, -oo)
                if not check_limit_at_inf(l_df):
                    return False
    except Exception:
        pass

    return True

def conditions(witness):
    # H1: X and Y are metric spaces (represented as sympy Sets)
    try:
        X = witness.get('X')
        Y = witness.get('Y')
        h1_ok = bool(isinstance(X, Set) and isinstance(Y, Set))
    except Exception:
        h1_ok = False

    # H2: A is a subset of X
    try:
        A = witness.get('A')
        X = witness.get('X')
        h2_ok = bool(isinstance(A, Set) and isinstance(X, Set) and A.is_subset(X) == True)
    except Exception:
        h2_ok = False

    # neg_Q: f|_A is NOT uniformly continuous on A
    try:
        A = witness.get('A')
        Y = witness.get('Y')
        f_expr = witness.get('f')
        
        if A is None or Y is None or f_expr is None:
            neg_q_ok = False
        else:
            sym = Symbol('x')
            if callable(f_expr):
                f_expr = f_expr(sym)
            elif isinstance(f_expr, (int, float)):
                f_expr = S(f_expr)
                
            free_syms = getattr(f_expr, 'free_symbols', set())
            if len(free_syms) == 1:
                sym = list(free_syms)[0]
            elif len(free_syms) > 1:
                sym = None
                
            if sym is None:
                neg_q_ok = False
            else:
                neg_q_ok = bool(not is_uniformly_continuous(f_expr, A, Y, sym))
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: (X, d_X) and (Y, d_Y) are metric spaces",
    "H_2: A is a subset of X equipped with the subspace metric",
    "¬Q: The restriction f|_A: A -> Y is not uniformly continuous on A"
]

N_HYP = 2
NEG_Q_INDEX = 2