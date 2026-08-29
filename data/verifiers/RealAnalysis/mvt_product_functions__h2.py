import sympy
from sympy.calculus.util import continuous_domain

x = sympy.Symbol('x', real=True)

def conditions(witness):
    try:
        f, g, a, b = witness
        f = sympy.sympify(f)
        g = sympy.sympify(g)
        a = sympy.sympify(a)
        b = sympy.sympify(b)
    except Exception:
        return [False, False, False]
        
    try:
        free_symbols = set()
        if hasattr(f, 'free_symbols'):
            free_symbols |= f.free_symbols
        if hasattr(g, 'free_symbols'):
            free_symbols |= g.free_symbols
            
        if len(free_symbols) == 1:
            var = list(free_symbols)[0]
        elif len(free_symbols) == 0:
            var = x
        else:
            if x in free_symbols:
                var = x
            else:
                var = list(free_symbols)[0]
    except Exception:
        var = x

    # H_1: f and g are continuous on [a, b]
    try:
        interval = sympy.Interval(a, b)
        f_cont = continuous_domain(f, var, interval)
        g_cont = continuous_domain(g, var, interval)
        h1 = interval.is_subset(f_cont) and interval.is_subset(g_cont)
    except Exception:
        h1 = False
        
    # H_2: a < b
    try:
        h2 = bool(a < b)
    except Exception:
        h2 = False
        
    # neg_Q: The conclusion fails for all c in (a, b)
    try:
        f_b = f.subs(var, b)
        f_a = f.subs(var, a)
        g_b = g.subs(var, b)
        g_a = g.subs(var, a)
        
        lhs = f_b * g_b - f_a * g_a
        
        df = f.diff(var)
        dg = g.diff(var)
        rhs = (df * g + f * dg) * (b - a)
        
        eq = sympy.Eq(rhs, lhs)
        
        has_valid_sol = False
        
        try:
            sols = sympy.solve(eq, var)
            if isinstance(sols, list):
                for c in sols:
                    try:
                        if c.is_real is False:
                            continue
                        c_val = float(c)
                        a_val = float(a)
                        b_val = float(b)
                        if a_val < c_val < b_val:
                            df_c = df.subs(var, c)
                            dg_c = dg.subs(var, c)
                            if df_c.is_finite and dg_c.is_finite:
                                has_valid_sol = True
                                break
                    except Exception:
                        pass
        except Exception:
            pass
            
        if not has_valid_sol:
            try:
                sset = sympy.solveset(eq, var, domain=sympy.Interval.open(a, b))
                if isinstance(sset, sympy.FiniteSet):
                    for c in sset:
                        try:
                            df_c = df.subs(var, c)
                            dg_c = dg.subs(var, c)
                            if df_c.is_finite and dg_c.is_finite:
                                has_valid_sol = True
                                break
                        except Exception:
                            pass
                elif not isinstance(sset, sympy.EmptySet) and not isinstance(sset, sympy.ConditionSet):
                    has_valid_sol = True
            except Exception:
                pass
                
        # Fallback: check a dense grid
        if not has_valid_sol:
            try:
                a_val = float(a)
                b_val = float(b)
                n_steps = 1000
                step = (b_val - a_val) / n_steps
                target = float(lhs) / (b_val - a_val)
                
                for i in range(1, n_steps):
                    c_val = a_val + i * step
                    try:
                        df_c = float(df.subs(var, c_val))
                        dg_c = float(dg.subs(var, c_val))
                        f_c = float(f.subs(var, c_val))
                        g_c = float(g.subs(var, c_val))
                        val = df_c * g_c + f_c * dg_c
                        
                        if abs(val - target) < 1e-7:
                            has_valid_sol = True
                            break
                    except Exception:
                        pass
            except Exception:
                pass

        neg_q = not has_valid_sol
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: f and g are continuous on the closed interval a to b",
    "H_2: a is less than b",
    "neg_Q: The conclusion fails for all c in the open interval a to b"
]

N_HYP = 2
NEG_Q_INDEX = 2