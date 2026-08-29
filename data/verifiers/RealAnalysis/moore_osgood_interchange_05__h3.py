import sympy
from sympy import Symbol, Interval, Union, oo, limit, AccumBounds, zoo, nan
from sympy.abc import x, n

# Top-level setup
# The symbols x and n are defined above and can be referenced in the witness expressions.

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false Moore-Osgood conjecture.
    
    The witness should be a dictionary with:
      'f_n': sympy expression in x and n
      'f': sympy expression in x
      'S': sympy Set (e.g., Interval)
      'x_0': real number or oo
    """
    
    # H_1: S is a subset of R and x_0 is a limit point of S
    try:
        S = witness['S']
        x_0 = witness['x_0']
        
        def is_limit_point(S, x_0):
            if x_0 == oo:
                try:
                    return S.sup == oo
                except Exception:
                    return False
            if x_0 == -oo:
                try:
                    return S.inf == -oo
                except Exception:
                    return False
            if isinstance(S, Interval):
                return S.inf <= x_0 <= S.sup and S.inf < S.sup
            if isinstance(S, Union):
                return any(is_limit_point(arg, x_0) for arg in S.args)
            return False
            
        h1_ok = S.is_subset(sympy.Reals) and is_limit_point(S, x_0)
    except Exception:
        h1_ok = False
        
    # H_2: {f_n} converges uniformly to f on S
    try:
        f_n = witness['f_n']
        f = witness['f']
        S = witness['S']
        
        diff = (f_n - f).simplify()
        if diff == 0:
            h2_ok = True
        else:
            h2_ok = False
            from sympy.calculus.util import maximum
            try:
                sup = maximum(abs(diff), x, S)
                if limit(sup, n, oo) == 0:
                    h2_ok = True
            except Exception:
                pass
            
            if not h2_ok:
                # Fallback numerical check for uniform convergence
                pts = []
                if S.is_Interval:
                    inf = float(S.inf) if S.inf != -oo else -100.0
                    sup = float(S.sup) if S.sup != oo else 100.0
                    for i in range(1, 50):
                        pts.append(inf + (sup - inf) * i / 50.0)
                
                max_errs = []
                for n_val in [10, 100, 1000]:
                    errs = []
                    current_pts = list(pts)
                    if S.is_Interval:
                        if S.sup != oo:
                            current_pts.append(float(S.sup) - 1.0/n_val)
                            current_pts.append(float(S.sup) - 0.1/n_val)
                        if S.inf != -oo:
                            current_pts.append(float(S.inf) + 1.0/n_val)
                            current_pts.append(float(S.inf) + 0.1/n_val)
                        try:
                            if S.contains(0):
                                current_pts.append(1.0/n_val)
                                current_pts.append(-1.0/n_val)
                        except Exception:
                            pass
                            
                    for pt in current_pts:
                        try:
                            if S.contains(pt):
                                val = abs(diff.subs({x: pt, n: n_val}).evalf())
                                errs.append(float(val))
                        except Exception:
                            pass
                    if errs:
                        max_errs.append(max(errs))
                
                if len(max_errs) == 3 and max_errs[-1] < 1e-2 and max_errs[-1] <= max_errs[0]:
                    h2_ok = True
    except Exception:
        h2_ok = False
        
    # ¬Q: The conclusion fails
    try:
        f_n = witness['f_n']
        f = witness['f']
        x_0 = witness['x_0']
        
        def limit_exists(expr, var, pt):
            try:
                L = limit(expr, var, pt)
                if L.has(AccumBounds) or L in (oo, -oo, zoo, nan):
                    return False, L
                return True, L
            except Exception:
                return None, None
                
        neg_q_ok = False
        
        # Check if L_n fails to exist for some specific n
        for n_val in [1, 2, 3]:
            f_n_val = f_n.subs(n, n_val)
            exists, _ = limit_exists(f_n_val, x, x_0)
            if exists is False:
                neg_q_ok = True
                break
                
        if not neg_q_ok:
            exists, L_n = limit_exists(f_n, x, x_0)
            if exists is False:
                neg_q_ok = True
            elif exists is True:
                exists_lim_L, lim_L_n = limit_exists(L_n, n, oo)
                if exists_lim_L is False:
                    neg_q_ok = True
                elif exists_lim_L is True:
                    exists_lim_f, lim_f = limit_exists(f, x, x_0)
                    if exists_lim_f is False:
                        neg_q_ok = True
                    elif exists_lim_f is True:
                        if lim_L_n.simplify() != lim_f.simplify():
                            neg_q_ok = True
    except Exception:
        neg_q_ok = False
        
    return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: S is a subset of R and x_0 is a limit point of S",
    "H_2: {f_n} converges uniformly to f on S",
    "¬Q: The conclusion fails (L_n does not converge, lim f(x) does not exist, or they are unequal)"
]

N_HYP = 2
NEG_Q_INDEX = 2