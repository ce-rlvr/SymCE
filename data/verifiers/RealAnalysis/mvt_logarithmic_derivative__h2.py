import sympy

x = sympy.Symbol('x', real=True)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False, False, False, False]
        f_expr, a_val, b_val = witness
        a = sympy.sympify(a_val)
        b = sympy.sympify(b_val)
        f = sympy.sympify(f_expr)
        
        free_syms = f.free_symbols
        if len(free_syms) > 1:
            if x not in free_syms:
                return [False, False, False, False]
        elif len(free_syms) == 1:
            sym = list(free_syms)[0]
            if sym != x:
                f = f.subs(sym, x)
    except Exception:
        return [False, False, False, False]

    h1 = False
    try:
        domain = sympy.calculus.util.continuous_domain(f, x, sympy.Interval(a, b))
        h1 = sympy.Interval(a, b).is_subset(domain)
        if h1 != True:
            sings = sympy.calculus.singularities(f, x, sympy.Interval(a, b))
            if sings.is_empty:
                h1 = True
    except Exception:
        try:
            sings = sympy.calculus.singularities(f, x, sympy.Interval(a, b))
            if sings.is_empty:
                h1 = True
        except Exception:
            h1 = False
    h1 = bool(h1)

    h2 = False
    try:
        zeros_and_neg = sympy.solveset(f <= 0, x, domain=sympy.Interval(a, b))
        if zeros_and_neg.is_empty:
            h2 = True
        elif isinstance(zeros_and_neg, sympy.ConditionSet):
            min_val = sympy.calculus.util.minimum(f, x, sympy.Interval(a, b))
            h2 = bool(min_val > 0)
    except Exception:
        try:
            min_val = sympy.calculus.util.minimum(f, x, sympy.Interval(a, b))
            h2 = bool(min_val > 0)
        except Exception:
            h2 = False

    h3 = False
    try:
        h3 = bool(a < b)
    except Exception:
        h3 = False

    neg_q = False
    try:
        fa = f.subs(x, a)
        fb = f.subs(x, b)
        rhs = (sympy.log(fb) - sympy.log(fa)) / (b - a)
        df = sympy.diff(f, x)
        eq = sympy.Eq(df / f, rhs)
        
        try:
            sols_set = sympy.solveset(eq, x, domain=sympy.Interval.open(a, b))
        except Exception:
            sols_set = sympy.ConditionSet(x, eq, sympy.Interval.open(a, b))
            
        def extract_points(s_set):
            pts = []
            try:
                if s_set.is_empty:
                    return pts
            except Exception:
                pass
            if isinstance(s_set, sympy.FiniteSet):
                pts.extend(list(s_set))
            elif isinstance(s_set, sympy.Interval):
                pts.append(s_set.mid)
            elif isinstance(s_set, sympy.Union):
                for arg in s_set.args:
                    pts.extend(extract_points(arg))
            else:
                try:
                    pts.extend(list(s_set))
                except Exception:
                    pass
            return pts

        sols = []
        if isinstance(sols_set, sympy.ConditionSet):
            try:
                sols_list = sympy.solve(eq, x)
                for s in sols_list:
                    sols.append(s)
            except Exception:
                pass
        else:
            sols = extract_points(sols_set)
            
        if not sols:
            try:
                eq2 = sympy.Eq(df, rhs * f)
                sols_set2 = sympy.solveset(eq2, x, domain=sympy.Interval.open(a, b))
                if not isinstance(sols_set2, sympy.ConditionSet):
                    sols.extend(extract_points(sols_set2))
                else:
                    sols_list2 = sympy.solve(eq2, x)
                    for s in sols_list2:
                        sols.append(s)
            except Exception:
                pass

        real_sols = []
        for s in sols:
            try:
                if s.is_real or abs(float(sympy.im(s))) < 1e-9:
                    val = sympy.re(s)
                    if a < val < b:
                        real_sols.append(val)
            except Exception:
                pass
        sols = real_sols

        unique_sols = []
        for s in sols:
            is_dup = False
            for us in unique_sols:
                try:
                    if abs(float(s - us)) < 1e-9:
                        is_dup = True
                        break
                except Exception:
                    pass
            if not is_dup:
                unique_sols.append(s)
        sols = unique_sols

        def check_sol(sol):
            try:
                df_val = df.subs(x, sol)
                f_val = f.subs(x, sol)
                val = df_val / f_val
                diff_val = val - rhs
                
                is_eq = False
                try:
                    if diff_val == 0 or diff_val.is_zero:
                        is_eq = True
                    elif abs(float(diff_val)) < 1e-7:
                        is_eq = True
                except Exception:
                    pass
                
                if not is_eq:
                    return False
                    
                sol_exact = sympy.nsimplify(sol) if isinstance(sol, sympy.Float) else sol
                
                limit_success = False
                try:
                    d_plus = sympy.limit((f - f.subs(x, sol_exact)) / (x - sol_exact), x, sol_exact, dir='+')
                    d_minus = sympy.limit((f - f.subs(x, sol_exact)) / (x - sol_exact), x, sol_exact, dir='-')
                    if d_plus != d_minus or not d_plus.is_real:
                        return False
                    limit_success = True
                except Exception:
                    pass
                    
                if not limit_success:
                    try:
                        h = 1e-7
                        sol_f = float(sol)
                        d_plus = (float(f.subs(x, sol_f + h)) - float(f.subs(x, sol_f))) / h
                        d_minus = (float(f.subs(x, sol_f)) - float(f.subs(x, sol_f - h))) / h
                        if abs(d_plus - d_minus) > 1e-3:
                            return False
                    except Exception:
                        pass
                        
                return True
            except Exception:
                pass
            return False

        valid_sols = False
        for sol in sols:
            if check_sol(sol):
                valid_sols = True
                break
                
        if not valid_sols:
            try:
                pts = [float(a) + i * (float(b) - float(a)) / 19 for i in range(1, 19)]
                for pt in pts:
                    try:
                        sol = sympy.nsolve(eq, x, pt)
                        if sol.is_real or abs(float(sympy.im(sol))) < 1e-9:
                            sol_re = sympy.re(sol)
                            if a < sol_re < b:
                                if check_sol(sol_re):
                                    valid_sols = True
                                    break
                    except Exception:
                        pass
            except Exception:
                pass
                
        neg_q = not valid_sols
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: f is continuous on the closed interval a to b",
    "H_2: f(x) > 0 for all x in the closed interval a to b",
    "H_3: a < b",
    "¬Q: There is no c in the open interval a to b such that df/f equals the difference quotient"
]

N_HYP = 3
NEG_Q_INDEX = 3