import sympy as sp

x, n = sp.symbols('x n', real=True)

CONDITION_LABELS = [
    "H_1: K is a compact subset of R",
    "H_2: The sequence (f_n) is uniformly equicontinuous on K",
    "H_3: The sequence (f_n) converges pointwise to a function f on K",
    "¬Q: The sequence (f_n) does not converge uniformly to f on K"
]

N_HYP = 3
NEG_Q_INDEX = 3

def check_not_uniform_convergence(f_n, f, x_sym, n_sym, K):
    diff = sp.Abs(f_n - f)
    
    try:
        dfn = sp.diff(f_n - f, x_sym)
        crit_pts = sp.solve(dfn, x_sym)
    except Exception:
        crit_pts = []
        
    test_pts = []
    if hasattr(K, 'is_Interval') and K.is_Interval:
        if K.start.is_finite:
            test_pts.extend([K.start, K.start + 1/n_sym, K.start + 1/sp.sqrt(n_sym)])
        else:
            test_pts.extend([-n_sym, -n_sym**2])
        if K.end.is_finite:
            test_pts.extend([K.end, K.end - 1/n_sym, K.end - 1/sp.sqrt(n_sym)])
        else:
            test_pts.extend([n_sym, n_sym**2])
    else:
        test_pts.extend([0, 1])
        
    if isinstance(crit_pts, list):
        test_pts.extend(crit_pts)
        
    for pt in test_pts:
        try:
            if pt.has(n_sym):
                try:
                    in_K = K.contains(pt.subs(n_sym, 100))
                except Exception:
                    in_K = False
                if in_K == True:
                    val = sp.limit(diff.subs(x_sym, pt), n_sym, sp.oo)
                    if val != 0:
                        try:
                            if abs(complex(val)) > 1e-9:
                                return True
                        except Exception:
                            return True
            else:
                if K.contains(pt) == True:
                    val = sp.limit(diff.subs(x_sym, pt), n_sym, sp.oo)
                    if val != 0:
                        try:
                            if abs(complex(val)) > 1e-9:
                                return True
                        except Exception:
                            return True
        except Exception:
            continue
            
    return False

def check_equicontinuous(f_n, f, x_sym, n_sym, K):
    try:
        df = sp.diff(f_n, x_sym)
    except Exception:
        return False
        
    if not df.has(n_sym):
        return True
        
    try:
        ddf = sp.diff(df, x_sym)
        crit_pts = sp.solve(ddf, x_sym)
    except Exception:
        crit_pts = []
        
    test_pts = []
    if hasattr(K, 'is_Interval') and K.is_Interval:
        if K.start.is_finite:
            test_pts.extend([K.start, K.start + 1/n_sym, K.start + 1/sp.sqrt(n_sym)])
        else:
            test_pts.extend([-n_sym, -n_sym**2])
        if K.end.is_finite:
            test_pts.extend([K.end, K.end - 1/n_sym, K.end - 1/sp.sqrt(n_sym)])
        else:
            test_pts.extend([n_sym, n_sym**2])
    else:
        test_pts.extend([0, 1])
        
    if isinstance(crit_pts, list):
        test_pts.extend(crit_pts)
    
    is_bounded = True
    for pt in test_pts:
        try:
            if pt.has(n_sym):
                try:
                    in_K = K.contains(pt.subs(n_sym, 100))
                except Exception:
                    in_K = False
                if in_K == True:
                    val = sp.limit(sp.Abs(df.subs(x_sym, pt)), n_sym, sp.oo)
                    if val in [sp.oo, -sp.oo, sp.zoo]:
                        is_bounded = False
                        break
            else:
                if K.contains(pt) == True:
                    val = sp.limit(sp.Abs(df.subs(x_sym, pt)), n_sym, sp.oo)
                    if val in [sp.oo, -sp.oo, sp.zoo]:
                        is_bounded = False
                        break
        except Exception:
            continue
            
    if is_bounded:
        return True
        
    # Fallback: if it converges uniformly to its pointwise limit, it is equicontinuous
    try:
        lim_f = sp.limit(f_n, n_sym, sp.oo)
        if not check_not_uniform_convergence(f_n, lim_f, x_sym, n_sym, K):
            return True
    except Exception:
        try:
            if not check_not_uniform_convergence(f_n, f, x_sym, n_sym, K):
                return True
        except Exception:
            pass
            
    return False

def check_pointwise_convergence(f_n, f, x_sym, n_sym, K):
    try:
        lim_f = sp.limit(f_n, n_sym, sp.oo)
        diff_val = sp.simplify(lim_f - f)
        if diff_val == 0:
            return True
    except Exception:
        pass
        
    test_pts = []
    if hasattr(K, 'is_Interval') and K.is_Interval:
        if K.start.is_finite and K.end.is_finite:
            w = K.end - K.start
            test_pts.extend([K.start + w*i/4 for i in range(5)])
        else:
            if K.start.is_finite:
                test_pts.extend([K.start + i for i in range(5)])
            elif K.end.is_finite:
                test_pts.extend([K.end - i for i in range(5)])
            else:
                test_pts.extend([0, 1, -1, 2, -2])
    else:
        test_pts.extend([0, 1, 2])
        
    for pt in test_pts:
        try:
            if K.contains(pt) == True:
                val_fn = sp.limit(f_n.subs(x_sym, pt), n_sym, sp.oo)
                val_f = f.subs(x_sym, pt)
                diff_val = sp.simplify(val_fn - val_f)
                if diff_val != 0:
                    try:
                        if abs(complex(diff_val)) > 1e-9:
                            return False
                    except Exception:
                        return False
        except Exception:
            pass
            
    return True

def conditions(witness):
    try:
        K = witness.get('K')
        f_n = witness.get('f_n')
        f = witness.get('f')
        x_sym = witness.get('x')
        n_sym = witness.get('n')
    except Exception:
        return [False, False, False, False]

    if any(v is None for v in [K, f_n, f, x_sym, n_sym]):
        return [False, False, False, False]

    # H1: K is a compact subset of R
    try:
        h1 = bool(K.is_subset(sp.S.Reals) and K.is_bounded and K.is_closed)
    except Exception:
        h1 = False

    # H2: The sequence (f_n) is uniformly equicontinuous on K
    try:
        h2 = check_equicontinuous(f_n, f, x_sym, n_sym, K)
    except Exception:
        h2 = False

    # H3: The sequence (f_n) converges pointwise to a function f on K
    try:
        h3 = check_pointwise_convergence(f_n, f, x_sym, n_sym, K)
    except Exception:
        h3 = False

    # neg_Q: The sequence (f_n) does NOT converge uniformly to f on K
    try:
        neg_q = check_not_uniform_convergence(f_n, f, x_sym, n_sym, K)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]