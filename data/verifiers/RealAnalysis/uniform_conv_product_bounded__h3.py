import sympy
from sympy import Symbol, Reals, Interval, sin, cos, pi, oo, Abs, limit, sympify, Expr, I
from sympy.calculus.util import maximum

x = Symbol('x', real=True)
n = Symbol('n', integer=True, positive=True)

def is_bounded(expr, x, n, S):
    import sympy
    from sympy.calculus.util import maximum
    from sympy import Abs, oo, limit
    
    try:
        expr_simp = sympy.simplify(expr)
    except Exception:
        expr_simp = expr
        
    if isinstance(S, sympy.FiniteSet):
        try:
            for pt in S:
                val = Abs(expr_simp).subs(x, pt)
                if val is oo:
                    return False
                if val.free_symbols:
                    lim_val = limit(val, n, oo)
                    if lim_val is oo or getattr(lim_val, 'upper', None) is oo:
                        return False
            return True
        except Exception:
            pass

    try:
        M = maximum(Abs(expr_simp), x, S)
        if M is oo:
            return False
        if M.free_symbols:
            lim_M = limit(M, n, oo)
            if lim_M is oo:
                return False
            if getattr(lim_M, 'upper', None) is oo:
                return False
            return True
        return True
    except Exception:
        pass
    
    try:
        if expr.is_bounded:
            return True
    except Exception:
        pass
        
    try:
        for i in range(1, 4):
            val = maximum(Abs(expr.subs(n, i)), x, S)
            if val is oo:
                return False
        return True
    except Exception:
        pass
        
    return False

def not_converges_uniformly(f_n, g_n, f, g, x, n, S):
    import sympy
    from sympy.calculus.util import maximum
    from sympy import Abs, limit, oo
    
    try:
        diff = Abs(f_n * g_n - f * g)
        try:
            diff = sympy.simplify(diff)
        except Exception:
            pass
        
        if isinstance(S, sympy.FiniteSet):
            for pt in S:
                pt_diff = diff.subs(x, pt)
                pt_lim = limit(pt_diff, n, oo)
                if pt_lim != 0:
                    if getattr(pt_lim, 'upper', None) is not None:
                        if pt_lim.upper > 0:
                            return True
                    else:
                        return True
            return False

        sup_diff = maximum(diff, x, S)
        if sup_diff is oo:
            return True
        lim = limit(sup_diff, n, oo)
        if lim == 0:
            return False
        if getattr(lim, 'upper', None) is not None:
            if lim.upper > 0:
                return True
            else:
                return False
        return True
    except Exception:
        pass
    
    try:
        for pt in [1, sympy.pi/4, sympy.pi/2, 0.5, 2]:
            if S.contains(pt) == True:
                pt_diff = diff.subs(x, pt)
                pt_lim = limit(pt_diff, n, oo)
                if pt_lim != 0:
                    if getattr(pt_lim, 'upper', None) is not None:
                        if pt_lim.upper > 0:
                            return True
                    else:
                        return True
    except Exception:
        pass
        
    return False

def conditions(witness):
    try:
        S, f_n, g_n, f, g = witness
    except Exception:
        return [False, False, False, False]
    
    import sympy
    from sympy import sympify, Expr, I
    
    try:
        f_n = sympify(f_n)
        g_n = sympify(g_n)
        f = sympify(f)
        g = sympify(g)
    except Exception:
        return [False, False, False, False]
    
    # H1: S is a subset of Reals
    try:
        from sympy import Reals
        h1 = bool(S.is_subset(Reals))
    except Exception:
        h1 = False
        
    # H2: f_n and g_n are sequences of functions from S to R
    try:
        h2 = isinstance(f_n, Expr) and isinstance(g_n, Expr) and not f_n.has(I) and not g_n.has(I)
    except Exception:
        h2 = False
        
    # H3: Boundedness
    try:
        h3 = is_bounded(f_n, x, n, S) and is_bounded(g_n, x, n, S)
    except Exception:
        h3 = False
        
    # Negated Conclusion: f_n g_n does NOT converge uniformly to f g on S
    try:
        neg_q = not_converges_uniformly(f_n, g_n, f, g, x, n, S)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: S is a subset of R",
    "H_2: f_n and g_n are sequences of functions from S to R",
    "H_3: f_n and g_n are uniformly bounded on S",
    "¬Q: f_n g_n does not converge uniformly to fg on S"
]

N_HYP = 3
NEG_Q_INDEX = 3