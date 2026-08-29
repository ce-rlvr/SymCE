import sympy
from sympy import Symbol, S, Interval, FiniteSet, Union, Abs, limit, oo, solve

# Top-level setup: named object bindings
x = Symbol('x', real=True)
n = Symbol('n', integer=True, positive=True)

CONDITION_LABELS = [
    "H_1: K is a compact metric space",
    "H_2: (f_n) is a sequence of continuous real-valued functions on K",
    "H_3: (f_n) converges uniformly to a continuous function f on K",
    "¬Q: There is no N and delta > 0 such that f_n(x) >= delta for all n >= N and x in K"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    H1_ok = False
    H2_ok = False
    H3_ok = False
    neg_Q_ok = False
    
    # H1: K is a compact metric space
    try:
        K = witness.get('K')
        if K is not None:
            H1_ok = bool(K.is_subset(S.Reals) and K.is_closed and K.is_bounded)
    except Exception:
        pass
        
    # H2: (f_n) is a sequence of continuous real-valued functions on K
    try:
        K = witness.get('K')
        f_n = witness.get('f_n')
        if K is not None and f_n is not None:
            from sympy.calculus.util import continuous_domain
            is_cont = True
            for i in [1, 2, 3, 4, 5]:
                f_n_i = f_n.subs(n, i)
                dom = continuous_domain(f_n_i, x, S.Reals)
                if not K.is_subset(dom):
                    is_cont = False
                    break
            H2_ok = is_cont
    except Exception:
        pass
        
    # H3: (f_n) converges uniformly to a continuous function f on K
    try:
        K = witness.get('K')
        f_n = witness.get('f_n')
        f = witness.get('f')
        if K is not None and f_n is not None and f is not None:
            from sympy.calculus.util import continuous_domain, maximum
            dom = continuous_domain(f, x, S.Reals)
            if K.is_subset(dom):
                diff_expr = f_n - f
                is_unif = False
                
                try:
                    max_val = maximum(Abs(diff_expr), x, K)
                    if limit(max_val, n, oo) == 0:
                        is_unif = True
                except Exception:
                    pass
                
                if not is_unif:
                    pts = []
                    if hasattr(K, 'start') and hasattr(K, 'end'):
                        pts.extend([K.start, K.end])
                        a, b = K.start, K.end
                    else:
                        if hasattr(K, 'boundary'):
                            pts.extend(list(K.boundary))
                        a, b = S.NegativeInfinity, S.Infinity
                        
                    deriv = diff_expr.diff(x)
                    if deriv != 0:
                        crit_pts = solve(deriv, x)
                        for pt in crit_pts:
                            pts.append(pt)
                            
                    is_unif_fallback = True
                    for pt in pts:
                        val = Abs(diff_expr.subs(x, pt))
                        lim_val = limit(val, n, oo)
                        if lim_val != 0:
                            try:
                                pt_lim = limit(pt, n, oo)
                                if a != S.NegativeInfinity and pt_lim < a:
                                    continue
                                if b != S.Infinity and pt_lim > b:
                                    continue
                            except Exception:
                                pass
                            is_unif_fallback = False
                            break
                    is_unif = is_unif_fallback
                
                H3_ok = is_unif
    except Exception:
        pass
        
    # neg_Q: The conclusion fails
    try:
        K = witness.get('K')
        f = witness.get('f')
        f_n = witness.get('f_n')
        
        neg_Q_evaluated = False
        
        if K is not None and f is not None:
            try:
                from sympy.calculus.util import minimum
                min_val = minimum(f, x, K)
                neg_Q_ok = bool(min_val <= 0)
                neg_Q_evaluated = True
            except Exception:
                try:
                    pts = []
                    if hasattr(K, 'start') and hasattr(K, 'end'):
                        pts.extend([K.start, K.end])
                    deriv = f.diff(x)
                    if deriv != 0:
                        crit_pts = solve(deriv, x)
                        for pt in crit_pts:
                            if pt.is_real and K.contains(pt):
                                pts.append(pt)
                    if pts:
                        min_val = min([f.subs(x, pt) for pt in pts])
                        neg_Q_ok = bool(min_val <= 0)
                        neg_Q_evaluated = True
                except Exception:
                    pass
                    
        if not neg_Q_evaluated and K is not None and f_n is not None:
            pts = []
            if hasattr(K, 'start') and hasattr(K, 'end'):
                pts.extend([K.start, K.end])
                a, b = K.start, K.end
            else:
                if hasattr(K, 'boundary'):
                    pts.extend(list(K.boundary))
                a, b = S.NegativeInfinity, S.Infinity
                
            deriv = f_n.diff(x)
            if deriv != 0:
                crit_pts = solve(deriv, x)
                for pt in crit_pts:
                    pts.append(pt)
            
            min_lim = oo
            for pt in pts:
                try:
                    pt_lim = limit(pt, n, oo)
                    if a != S.NegativeInfinity and pt_lim < a:
                        continue
                    if b != S.Infinity and pt_lim > b:
                        continue
                except Exception:
                    pass
                
                val = f_n.subs(x, pt)
                lim_val = limit(val, n, oo)
                if lim_val < min_lim:
                    min_lim = lim_val
                    
            if min_lim != oo:
                neg_Q_ok = bool(min_lim <= 0)
    except Exception:
        pass
        
    return [H1_ok, H2_ok, H3_ok, neg_Q_ok]