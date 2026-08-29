import sympy
from sympy import Symbol, Interval, Union, FiniteSet, Reals, oo, Abs, limit, solve
from sympy.calculus.util import continuous_domain, maximum
from sympy.calculus.singularities import singularities

x = Symbol('x', real=True)

def conditions(witness):
    try:
        K, f = witness
    except Exception:
        return [False, False]
        
    # H_1: K is a compact subset of R
    h1_ok = False
    try:
        if K.is_subset(Reals) == True and K.is_bounded == True and K.is_closed == True:
            h1_ok = True
    except Exception:
        h1_ok = False
        
    # neg_Q: f is NOT globally Lipschitz continuous on K
    neg_q_ok = False
    try:
        if isinstance(K, FiniteSet):
            for p in K:
                if not f.subs(x, p).is_finite:
                    neg_q_ok = True
                    break
            return [h1_ok, neg_q_ok]

        # 1. Check if f is not continuous on K
        try:
            dom = continuous_domain(f, x, Reals)
            if not dom.contains(K):
                neg_q_ok = True
        except Exception:
            pass
            
        if not neg_q_ok:
            df = sympy.diff(f, x)
            
            # 2. Check maximum of Abs(df)
            try:
                max_val = maximum(Abs(df), x, K)
                if max_val == oo:
                    neg_q_ok = True
            except Exception:
                pass
                
        if not neg_q_ok:
            # 3. Check limits at boundary points
            pts = []
            if isinstance(K, Interval):
                pts = [K.start, K.end]
            elif isinstance(K, Union):
                for arg in K.args:
                    if isinstance(arg, Interval):
                        pts.extend([arg.start, arg.end])
            for p in pts:
                try:
                    if limit(Abs(df), x, p, dir='+') == oo or limit(Abs(df), x, p, dir='-') == oo:
                        neg_q_ok = True
                        break
                except Exception:
                    pass
                    
        if not neg_q_ok:
            # 4. Check roots of denominator of df
            try:
                n, d = sympy.cancel(df).as_numer_denom()
                zeros = solve(d, x)
                if isinstance(zeros, dict):
                    zeros = list(zeros.keys())
                for z in zeros:
                    if z.is_real and z in K:
                        try:
                            L_plus = limit(Abs(df), x, z, dir='+')
                            L_minus = limit(Abs(df), x, z, dir='-')
                            if L_plus == oo or L_minus == oo:
                                neg_q_ok = True
                                break
                            elif L_plus.is_finite and L_minus.is_finite:
                                continue
                        except Exception:
                            pass
                        
                        if not neg_q_ok:
                            try:
                                if n.subs(x, z) != 0:
                                    neg_q_ok = True
                                    break
                            except Exception:
                                neg_q_ok = True
                                break
            except Exception:
                pass
                
        if not neg_q_ok:
            # 5. Check singularities of df
            try:
                sings = singularities(df, x)
                if isinstance(sings, sympy.Set):
                    for s in sings:
                        if s in K:
                            try:
                                L_plus = limit(Abs(df), x, s, dir='+')
                                L_minus = limit(Abs(df), x, s, dir='-')
                                if L_plus == oo or L_minus == oo:
                                    neg_q_ok = True
                                    break
                                elif L_plus.is_finite and L_minus.is_finite:
                                    continue
                            except Exception:
                                pass
                            
                            if not neg_q_ok:
                                neg_q_ok = True
                                break
            except Exception:
                pass
                
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: K is a compact subset of R",
    "¬Q: f is not globally Lipschitz continuous on K"
]

N_HYP = 1
NEG_Q_INDEX = 1