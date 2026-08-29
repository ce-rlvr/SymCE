import sympy
from sympy.abc import x

# Top-level setup
# No specific named groups needed for RealAnalysis

CONDITION_LABELS = [
    "H_1: f is continuous on [a, oo)",
    "H_2: lim_{x -> oo} f(x) = f(a)",
    "¬Q: There is no c in (a, oo) such that f'(c) = 0"
]

N_HYP = 2
NEG_Q_INDEX = 2

def is_continuous_on_interval(f, x, a):
    try:
        fa = f.subs(x, a)
        if not fa.is_real or fa.has(sympy.oo, sympy.zoo, -sympy.oo, sympy.nan):
            return False
    except Exception:
        return False

    try:
        from sympy.calculus.util import continuous_domain
        dom = continuous_domain(f, x, sympy.Interval(a, sympy.oo))
        if sympy.Interval(a, sympy.oo).is_subset(dom):
            return True
    except Exception:
        pass

    try:
        sings = sympy.singularities(f, x)
        for s in sings:
            if s.is_real and s >= a:
                return False
    except Exception:
        pass

    try:
        points_to_check = set()
        
        def extract_relational_bounds(condition):
            bounds = set()
            if isinstance(condition, sympy.Relational):
                try:
                    eq = sympy.Eq(condition.lhs, condition.rhs)
                    sols = sympy.solveset(eq, x, domain=sympy.S.Reals)
                    if isinstance(sols, sympy.FiniteSet):
                        for sol in sols:
                            if sol.is_real and sol >= a:
                                bounds.add(sol)
                except Exception:
                    pass
            elif isinstance(condition, (sympy.And, sympy.Or)):
                for arg in condition.args:
                    bounds.update(extract_relational_bounds(arg))
            return bounds

        for arg in f.atoms(sympy.Piecewise):
            for expr, cond in arg.args:
                points_to_check.update(extract_relational_bounds(cond))
        
        for arg in f.atoms(sympy.Abs):
            try:
                sols = sympy.solveset(arg.args[0], x, domain=sympy.S.Reals)
                if isinstance(sols, sympy.FiniteSet):
                    for sol in sols:
                        if sol.is_real and sol >= a:
                            points_to_check.add(sol)
            except Exception:
                pass

        for pt in points_to_check:
            lim_right = sympy.limit(f, x, pt, dir='+')
            val = f.subs(x, pt)
            if val != lim_right:
                return False
            if pt > a:
                lim_left = sympy.limit(f, x, pt, dir='-')
                if lim_left != lim_right:
                    return False
    except Exception:
        pass

    try:
        for i in range(100):
            val = a + i * 0.137
            v = f.subs(x, val).evalf()
            if not v.is_real or abs(v) > 1e10:
                return False
    except Exception:
        return False

    return True

def check_h2(f, x, a):
    try:
        fa = f.subs(x, a)
        lim = sympy.limit(f, x, sympy.oo)
        if lim == fa:
            return True
        if sympy.simplify(lim - fa) == 0:
            return True
        return False
    except Exception:
        return False

def derivative_exists_and_zero(f, x, c):
    try:
        if not c.is_real:
            return False
            
        fc = f.subs(x, c)
        dq = (f - fc) / (x - c)
        lim_left = sympy.limit(dq, x, c, dir='-')
        lim_right = sympy.limit(dq, x, c, dir='+')
        
        if lim_left == 0 and lim_right == 0:
            return True
        return False
    except Exception:
        try:
            df = sympy.diff(f, x)
            df_left = df.subs(x, c - 1e-7).evalf()
            df_right = df.subs(x, c + 1e-7).evalf()
            if abs(df_left) < 1e-5 and abs(df_right) < 1e-5:
                return True
        except Exception:
            pass
        return False

def check_neg_q(f, x, a):
    try:
        df = sympy.diff(f, x)
        
        sol_set = sympy.solveset(df, x, domain=sympy.Interval.Lopen(a, sympy.oo))
        
        if sol_set == sympy.S.EmptySet:
            return True
            
        if isinstance(sol_set, sympy.FiniteSet):
            for c in sol_set:
                if c > a and derivative_exists_and_zero(f, x, c):
                    return False
            return True
            
        if isinstance(sol_set, sympy.Interval):
            if sol_set.end == sympy.oo:
                c = sol_set.start + 1
            else:
                c = sol_set.start + (sol_set.end - sol_set.start) / 2
            if c > a and derivative_exists_and_zero(f, x, c):
                return False
                
        if isinstance(sol_set, sympy.Union):
            for arg in sol_set.args:
                if isinstance(arg, sympy.FiniteSet):
                    for c in arg:
                        if c > a and derivative_exists_and_zero(f, x, c):
                            return False
                elif isinstance(arg, sympy.Interval):
                    if arg.end == sympy.oo:
                        c = arg.start + 1
                    else:
                        c = arg.start + (arg.end - arg.start) / 2
                    if c > a and derivative_exists_and_zero(f, x, c):
                        return False
            return True

    except Exception:
        pass

    try:
        sols = sympy.solve(df, x)
        if isinstance(sols, list):
            for c in sols:
                if c.is_real and c > a:
                    if derivative_exists_and_zero(f, x, c):
                        return False
            return True
    except Exception:
        pass

    try:
        prev_sign = None
        for i in range(1, 1000):
            val = a + i * 0.137
            try:
                df_val = df.subs(x, val).evalf()
            except Exception:
                continue
                
            if not df_val.is_real:
                continue
                
            if abs(df_val) < 1e-7:
                if derivative_exists_and_zero(f, x, val):
                    return False
            
            curr_sign = 1 if df_val > 0 else -1 if df_val < 0 else 0
            if prev_sign is not None and curr_sign != prev_sign and curr_sign != 0 and prev_sign != 0:
                left = val - 0.137
                right = val
                for _ in range(30):
                    mid = (left + right) / 2
                    try:
                        mid_val = df.subs(x, mid).evalf()
                    except Exception:
                        break
                    if not mid_val.is_real:
                        break
                    if abs(mid_val) < 1e-7:
                        if derivative_exists_and_zero(f, x, mid):
                            return False
                        break
                    if (mid_val > 0) == (curr_sign > 0):
                        right = mid
                    else:
                        left = mid
                mid = (left + right) / 2
                if derivative_exists_and_zero(f, x, mid):
                    return False
            prev_sign = curr_sign
        return True
    except Exception:
        pass

    return False

def conditions(witness):
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False, False]
        f_expr, a_val = witness
        
        f_expr = sympy.sympify(f_expr)
        a_val = sympy.sympify(a_val)
        
        h1 = bool(is_continuous_on_interval(f_expr, x, a_val))
    except Exception:
        h1 = False

    try:
        h2 = bool(check_h2(f_expr, x, a_val))
    except Exception:
        h2 = False

    try:
        neg_q = bool(check_neg_q(f_expr, x, a_val))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]