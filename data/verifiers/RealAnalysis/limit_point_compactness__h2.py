import sympy
from sympy import Symbol, Lambda, oo, Interval, Union, Intersection, ProductSet, ImageSet, FiniteSet

# Top-level setup for standard Real Analysis objects
Reals = sympy.S.Reals
Integers = sympy.S.Integers
Naturals = sympy.S.Naturals
Rationals = sympy.S.Rationals

def check_metric(X, d):
    points = []
    if hasattr(X, 'is_subset') and X.is_subset(sympy.S.Reals):
        for p in [0, 1, -1, sympy.pi, sympy.Rational(1, 2), 2, 3]:
            if p in X:
                points.append(p)
    if not points and hasattr(X, 'start') and hasattr(X, 'end'):
        try:
            if X.start.is_real: points.append(X.start)
            if X.end.is_real: points.append(X.end)
            mid = (X.start + X.end) / 2
            if mid.is_real: points.append(mid)
        except Exception:
            pass
            
    if not points:
        if isinstance(X, sympy.FiniteSet):
            points = list(X)
            
    if not points:
        return callable(d)
        
    evaluated_any = False
    for x in points:
        for y in points:
            try:
                d_xy = float(d(x, y))
                evaluated_any = True
                if d_xy < -1e-9: return False
                if x == y and d_xy > 1e-9: return False
                if x != y and d_xy < 1e-9: return False
                d_yx = float(d(y, x))
                if abs(d_xy - d_yx) > 1e-9: return False
                for z in points:
                    d_xz = float(d(x, z))
                    d_yz = float(d(y, z))
                    if d_xz > d_xy + d_yz + 1e-9: return False
            except Exception:
                return False
    return evaluated_any

def has_limit_points(S, X):
    if S.is_finite is True:
        return False
    if S.is_finite is None and isinstance(S, sympy.ImageSet):
        syms = list(S.expr.free_symbols)
        if len(syms) == 1:
            v = syms[0]
            try:
                vals = {S.expr.subs(v, i) for i in range(1, 10)}
                if len(vals) <= 5:
                    return False
            except Exception:
                pass

    if S in (sympy.S.Integers, sympy.S.Naturals, sympy.S.Naturals0):
        return False
    if isinstance(S, sympy.Interval):
        return True
    if isinstance(S, sympy.Union):
        return any(has_limit_points(arg, X) for arg in S.args)
    if isinstance(S, sympy.ProductSet):
        if isinstance(X, sympy.ProductSet) and len(X.args) == len(S.args):
            X_args = X.args
        else:
            X_args = [sympy.S.Reals] * len(S.args)
        return any(has_limit_points(s_arg, x_arg) for s_arg, x_arg in zip(S.args, X_args))
    if isinstance(S, sympy.ImageSet):
        expr = S.expr
        base = S.base_set
        if base in (sympy.S.Naturals, sympy.S.Naturals0, sympy.S.Integers):
            syms = list(expr.free_symbols)
            if len(syms) == 1:
                n = syms[0]
                try:
                    lim_pos = sympy.limit(expr, n, sympy.oo)
                    if lim_pos.is_real:
                        in_X = lim_pos in X
                        if in_X is True:
                            return True
                        elif in_X is None:
                            if isinstance(X, sympy.Interval):
                                if X.left_open and lim_pos <= X.start: return False
                                if not X.left_open and lim_pos < X.start: return False
                                if X.right_open and lim_pos >= X.end: return False
                                if not X.right_open and lim_pos > X.end: return False
                                return True
                            return True
                    else:
                        if lim_pos != sympy.oo and lim_pos != -sympy.oo:
                            return True
                except Exception:
                    return True
                    
                if base == sympy.S.Integers:
                    try:
                        lim_neg = sympy.limit(expr, n, -sympy.oo)
                        if lim_neg.is_real:
                            in_X = lim_neg in X
                            if in_X is True:
                                return True
                            elif in_X is None:
                                if isinstance(X, sympy.Interval):
                                    if X.left_open and lim_neg <= X.start: return False
                                    if not X.left_open and lim_neg < X.start: return False
                                    if X.right_open and lim_neg >= X.end: return False
                                    if not X.right_open and lim_neg > X.end: return False
                                    return True
                                return True
                        else:
                            if lim_neg != sympy.oo and lim_neg != -sympy.oo:
                                return True
                    except Exception:
                        return True
                return False
    return True

def conditions(witness):
    if isinstance(witness, tuple):
        if len(witness) == 3:
            X, d, S = witness
        elif len(witness) == 2:
            X, S = witness
            d = lambda x, y: sympy.Abs(x - y)
        else:
            return [False, False, False]
    else:
        return [False, False, False]
        
    try:
        h1 = check_metric(X, d)
    except Exception:
        h1 = False
        
    try:
        subset_check = S.is_subset(X)
        if subset_check is None:
            if X == sympy.S.Reals:
                subset_check = True
            elif isinstance(S, sympy.ImageSet):
                syms = list(S.expr.free_symbols)
                if len(syms) == 1:
                    v = syms[0]
                    subset_check = True
                    for i in [1, 2, 3, 10, 100]:
                        val = S.expr.subs(v, i)
                        in_X = val in X
                        if in_X is False:
                            subset_check = False
                            break
                        elif in_X is None and isinstance(X, sympy.Interval):
                            if X.left_open and val <= X.start: subset_check = False; break
                            if not X.left_open and val < X.start: subset_check = False; break
                            if X.right_open and val >= X.end: subset_check = False; break
                            if not X.right_open and val > X.end: subset_check = False; break
            elif isinstance(S, sympy.ProductSet):
                if isinstance(X, sympy.ProductSet) and len(X.args) == len(S.args):
                    subset_check = all(s.is_subset(x) for s, x in zip(S.args, X.args))
        
        if subset_check is None:
            subset_check = False
            
        finite_check = S.is_finite
        if finite_check is None:
            if isinstance(S, sympy.ImageSet):
                syms = list(S.expr.free_symbols)
                if len(syms) == 1:
                    v = syms[0]
                    try:
                        vals = {S.expr.subs(v, i) for i in range(1, 10)}
                        finite_check = len(vals) <= 5
                    except Exception:
                        finite_check = False
            elif isinstance(S, sympy.ProductSet):
                finite_check = False
                
        h2 = bool(subset_check) and (finite_check is False)
    except Exception:
        h2 = False
        
    try:
        neg_q = not has_limit_points(S, X)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: (X, d) is a metric space",
    "H_2: S is an infinite subset of X",
    "¬Q: S has no limit points in X"
]

N_HYP = 2
NEG_Q_INDEX = 2