import sympy
import math

x = sympy.Symbol('x', real=True)

def check_continuity(f, x_sym, a, b):
    try:
        if float(a) >= float(b):
            return False
    except Exception:
        return False

    try:
        from sympy.calculus.util import continuous_domain
        domain = continuous_domain(f, x_sym, sympy.Interval(a, b))
        if domain != sympy.Interval(a, b):
            return False
    except Exception:
        pass

    try:
        val_a = f.subs(x_sym, a)
        val_b = f.subs(x_sym, b)
        if not val_a.is_real or not val_b.is_real:
            return False
    except Exception:
        return False

    try:
        lim_a = sympy.limit(f, x_sym, a, dir='+')
        if sympy.simplify(lim_a - val_a) != 0:
            return False
    except Exception:
        pass

    try:
        lim_b = sympy.limit(f, x_sym, b, dir='-')
        if sympy.simplify(lim_b - val_b) != 0:
            return False
    except Exception:
        pass

    try:
        from sympy.calculus.singularities import singularities
        sings = singularities(f, x_sym)
        if isinstance(sings, sympy.Set):
            inter = sings.intersect(sympy.Interval(a, b))
            if not inter.is_empty:
                return False
    except Exception:
        pass

    try:
        f_lam = sympy.lambdify(x_sym, f, modules=['math'])
        n_points = 1000
        step = float(b - a) / n_points
        for i in range(1, n_points):
            pt = float(a) + i * step
            val = f_lam(pt)
            if not isinstance(val, (int, float)):
                return False
            if math.isnan(val) or math.isinf(val):
                return False
    except Exception:
        pass

    return True

def check_conclusion(f, x_sym, a, b):
    try:
        slope = sympy.simplify((f.subs(x_sym, b) - f.subs(x_sym, a)) / (b - a))
    except Exception:
        return False
        
    df = sympy.diff(f, x_sym)
    
    sols = set()
    
    try:
        if sympy.simplify(df - slope) == 0:
            sols.add((a + b) / 2)
    except Exception:
        pass

    try:
        ss = sympy.solveset(sympy.Eq(df, slope), x_sym, domain=sympy.Interval.open(a, b))
        if isinstance(ss, sympy.FiniteSet):
            sols.update(ss)
        elif ss == sympy.S.EmptySet:
            pass
        elif isinstance(ss, sympy.Interval):
            sols.add(ss.mid)
        elif isinstance(ss, sympy.Union):
            for arg in ss.args:
                if isinstance(arg, sympy.FiniteSet):
                    sols.update(arg)
                elif isinstance(arg, sympy.Interval):
                    sols.add(arg.mid)
    except Exception:
        pass

    try:
        list_sols = sympy.solve(sympy.Eq(df, slope), x_sym)
        for s in list_sols:
            if s.is_real and a < s < b:
                sols.add(s)
    except Exception:
        pass

    h = sympy.Symbol('h', real=True)
    
    for c in sols:
        try:
            if not (a < c < b):
                continue
            
            diff_quotient = (f.subs(x_sym, c+h) - f.subs(x_sym, c)) / h
            lim_plus = sympy.limit(diff_quotient, h, 0, dir='+')
            lim_minus = sympy.limit(diff_quotient, h, 0, dir='-')
            
            if lim_plus == lim_minus and lim_plus.is_real:
                if sympy.simplify(lim_plus - slope) == 0:
                    return False
        except Exception:
            try:
                c_val = float(c)
                h_val = 1e-7
                dq_plus = float((f.subs(x_sym, c_val+h_val) - f.subs(x_sym, c_val)) / h_val)
                dq_minus = float((f.subs(x_sym, c_val) - f.subs(x_sym, c_val-h_val)) / h_val)
                if abs(dq_plus - dq_minus) < 1e-4:
                    if abs(dq_plus - float(slope)) < 1e-4:
                        return False
            except Exception:
                pass

    try:
        f_lam = sympy.lambdify(x_sym, f, modules=['math'])
        n_points = 20000
        step = float(b - a) / n_points
        slope_f = float(slope)
        for i in range(1, n_points):
            c_val = float(a) + i * step
            h_val = 1e-6
            try:
                f_plus = float(f_lam(c_val + h_val))
                f_minus = float(f_lam(c_val - h_val))
                f_c = float(f_lam(c_val))
                
                dq_plus = (f_plus - f_c) / h_val
                dq_minus = (f_c - f_minus) / h_val
                
                if abs(dq_plus - dq_minus) < 1e-3:
                    if abs(dq_plus - slope_f) < 1e-3:
                        h2 = 1e-8
                        f_p2 = float(f_lam(c_val + h2))
                        f_m2 = float(f_lam(c_val - h2))
                        dq_p2 = (f_p2 - f_c) / h2
                        dq_m2 = (f_c - f_m2) / h2
                        if abs(dq_p2 - dq_m2) < 1e-3 and abs(dq_p2 - slope_f) < 1e-3:
                            return False
            except Exception:
                continue
    except Exception:
        pass

    return True

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False, False]
        f, a, b = witness
    except Exception:
        return [False, False]

    try:
        if not isinstance(f, sympy.Expr):
            return [False, False]
        
        free_syms = f.free_symbols
        if len(free_syms) == 1:
            x_sym = list(free_syms)[0]
        elif len(free_syms) == 0:
            x_sym = sympy.Symbol('x', real=True)
        else:
            x_syms = [s for s in free_syms if s.name == 'x']
            if x_syms:
                x_sym = x_syms[0]
            else:
                return [False, False]
                
        if not x_sym.is_real:
            x_real = sympy.Symbol(x_sym.name, real=True)
            f = f.subs(x_sym, x_real)
            x_sym = x_real
            
    except Exception:
        return [False, False]

    try:
        h1 = check_continuity(f, x_sym, a, b)
    except Exception:
        h1 = False

    try:
        neg_q = check_conclusion(f, x_sym, a, b)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = ["H_1: f is continuous on the closed interval", "not Q: No c in the open interval has derivative equal to the difference quotient"]
N_HYP = 1
NEG_Q_INDEX = 1