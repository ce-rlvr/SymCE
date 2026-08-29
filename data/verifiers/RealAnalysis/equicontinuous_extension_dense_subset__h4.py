import sympy
from sympy import Symbol, Interval, S, limit, diff, AccumBounds

# Top-level setup
# (No specific named objects needed for this real analysis domain)

def conditions(witness):
    try:
        X = witness['X']
        Y = witness['Y']
        D = witness['D']
        F = witness['F']
        if not isinstance(F, list):
            F = [F]
        x_obj = witness['x']
        if isinstance(x_obj, str):
            x = Symbol(x_obj)
        else:
            x = x_obj
    except KeyError:
        return [False, False, False, False]

    # H1: X is a metric space (we assume subsets of Reals are metric spaces)
    try:
        h1 = (X.is_subset(S.Reals) == True)
    except Exception:
        h1 = False

    # H2: Y is a complete metric space (closed subset of Reals)
    try:
        h2 = (Y.is_subset(S.Reals) == True) and (Y.is_closed == True or Y.closure == Y)
    except Exception:
        h2 = False

    # H3: D is a dense subset of X
    try:
        h3 = (D.is_subset(X) == True) and (X.is_subset(D.closure) == True)
    except Exception:
        h3 = False

    # neg_Q: Conclusion fails
    # The conclusion is that each f in F has a unique continuous extension to X into Y,
    # and the family of extensions is uniformly equicontinuous on X.
    neg_q = False
    try:
        missing_points = X - D
        if missing_points.is_FiniteSet:
            points_to_check = list(missing_points)
        else:
            points_to_check = []
            
        boundary_points = set()
        try:
            closure_minus_X = X.closure - X
            if closure_minus_X.is_FiniteSet:
                for p in closure_minus_X:
                    if p.is_real and not p.has(S.Infinity, S.NegativeInfinity):
                        boundary_points.add(p)
        except Exception:
            pass
            
        for f in F:
            extension_valid = True
            
            # 1. Check if continuous extension to X exists and maps to Y
            for p in points_to_check:
                if p is None or not p.is_real:
                    continue
                
                if isinstance(X, Interval):
                    if p == X.inf:
                        lim = limit(f, x, p, dir='+')
                    elif p == X.sup:
                        lim = limit(f, x, p, dir='-')
                    else:
                        lim = limit(f, x, p)
                else:
                    lim = limit(f, x, p)
                
                if isinstance(lim, AccumBounds) or lim.has(S.Infinity, S.NegativeInfinity, S.NaN, S.ComplexInfinity):
                    extension_valid = False
                    break
                
                try:
                    contains = Y.contains(lim)
                    if contains == False:
                        extension_valid = False
                        break
                except Exception:
                    extension_valid = False
                    break
            
            if not extension_valid:
                neg_q = True
                break
                
            # 2. Check uniform continuity on X
            # For bounded intervals, a continuous function is uniformly continuous iff it extends continuously to the closure.
            for p in boundary_points:
                if isinstance(X, Interval):
                    if p == X.inf:
                        lim = limit(f, x, p, dir='+')
                    elif p == X.sup:
                        lim = limit(f, x, p, dir='-')
                    else:
                        lim = limit(f, x, p)
                else:
                    lim = limit(f, x, p)
                    
                if isinstance(lim, AccumBounds) or lim.has(S.Infinity, S.NegativeInfinity, S.NaN, S.ComplexInfinity):
                    extension_valid = False
                    break
                    
            if not extension_valid:
                neg_q = True
                break
                
            # For unbounded X, check if the derivative is bounded at infinity
            if getattr(X, 'sup', None) == S.Infinity or getattr(X, 'inf', None) == S.NegativeInfinity:
                df = diff(f, x)
                if getattr(X, 'sup', None) == S.Infinity:
                    lim_f = limit(f, x, S.Infinity)
                    # If the function itself doesn't have a finite limit at infinity, check its derivative
                    if isinstance(lim_f, AccumBounds) or lim_f.has(S.Infinity, S.NegativeInfinity, S.NaN, S.ComplexInfinity):
                        lim_df = limit(df, x, S.Infinity)
                        if lim_df.has(S.Infinity, S.NegativeInfinity, S.ComplexInfinity):
                            neg_q = True
                            break
                if getattr(X, 'inf', None) == S.NegativeInfinity:
                    lim_f = limit(f, x, S.NegativeInfinity)
                    if isinstance(lim_f, AccumBounds) or lim_f.has(S.Infinity, S.NegativeInfinity, S.NaN, S.ComplexInfinity):
                        lim_df = limit(df, x, S.NegativeInfinity)
                        if lim_df.has(S.Infinity, S.NegativeInfinity, S.ComplexInfinity):
                            neg_q = True
                            break
                            
    except Exception:
        pass

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: X is a metric space",
    "H_2: Y is a complete metric space",
    "H_3: D is a dense subset of X",
    "¬Q: The family of extensions is not uniformly equicontinuous or an extension does not exist"
]

N_HYP = 3
NEG_Q_INDEX = 3