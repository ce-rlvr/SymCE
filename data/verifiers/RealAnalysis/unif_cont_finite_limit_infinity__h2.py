import sympy
import math

x = sympy.Symbol('x', real=True)

def parse_witness(witness):
    global x
    if isinstance(witness, tuple):
        if len(witness) == 2:
            f, a = witness
        else:
            f = witness[0]
            a = sympy.S(0)
    else:
        f = witness
        a = sympy.S(0)
        
    if callable(f):
        try:
            f = f(x)
        except Exception:
            pass
    else:
        try:
            if isinstance(f, str):
                f = sympy.sympify(f, locals={'x': x})
            free_symbols = f.free_symbols
            if len(free_symbols) == 1:
                sym = list(free_symbols)[0]
                if sym != x:
                    f = f.subs(sym, x)
        except Exception:
            pass
            
    return f, sympy.sympify(a), x

def is_continuous_on(f, x, a):
    try:
        a_val = sympy.sympify(a)
        if not a_val.is_real:
            return False
            
        domain = sympy.calculus.util.continuous_domain(f, x, sympy.S.Reals)
        interval = sympy.Interval(a_val, sympy.oo)
        if interval.is_subset(domain) == True:
            return True
        if interval.intersection(domain).is_empty == True:
            return False
    except Exception:
        pass

    try:
        sings = sympy.calculus.singularities(f, x)
        interval = sympy.Interval(a_val, sympy.oo)
        if sings.intersection(interval).is_empty == False:
            return False
    except Exception:
        pass

    try:
        f_lam = sympy.lambdify(x, f, modules=['math'])
        a_f = float(a_val)
        for i in range(1000):
            pt = a_f + i * 0.1
            val = f_lam(pt)
            if isinstance(val, complex):
                return False
            if math.isnan(val) or math.isinf(val):
                return False
        return True
    except Exception:
        pass

    return False

def is_uniformly_continuous(f, x, a):
    try:
        L = sympy.limit(f, x, sympy.oo)
        if L.is_finite:
            return True
    except Exception:
        pass

    try:
        c = sympy.limit(f / x, x, sympy.oo)
        if c.is_finite:
            d = sympy.limit(f - c * x, x, sympy.oo)
            if d.is_finite:
                return True
    except Exception:
        pass

    df = None
    try:
        df = sympy.diff(f, x)
        L_df = sympy.limit(sympy.Abs(df), x, sympy.oo)
        if L_df.is_finite:
            return True
        if L_df == sympy.oo:
            return False
    except Exception:
        pass

    try:
        if f.is_polynomial(x):
            if sympy.degree(f, x) >= 2:
                return False
            else:
                return True
    except Exception:
        pass

    if df is not None:
        try:
            f_lam = sympy.lambdify(x, f, modules=['math'])
            df_lam = sympy.lambdify(x, df, modules=['math'])
            
            epsilon = 0.1
            p_n_max = 1.0
            
            violations = 0
            for xv in [1e2, 1e3, 1e4, 1e5, 1e6, 1e7]:
                max_df = 0
                best_x = xv
                for dx in [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5, 6.0]:
                    try:
                        val = abs(df_lam(xv + dx))
                        if val > max_df:
                            max_df = val
                            best_x = xv + dx
                    except Exception:
                        pass
                
                if max_df > 0:
                    p_n = 2 * epsilon / max_df
                    if p_n < p_n_max:
                        try:
                            diff = abs(f_lam(best_x + p_n) - f_lam(best_x))
                            if diff >= epsilon / 2:
                                violations += 1
                                p_n_max = p_n
                        except Exception:
                            pass
            
            if violations >= 3:
                return False
        except Exception:
            pass

    return True

def conditions(witness):
    try:
        f, a, x_sym = parse_witness(witness)
    except Exception:
        return [False, False]
        
    try:
        h1 = is_continuous_on(f, x_sym, a)
    except Exception:
        h1 = False
        
    try:
        neg_q = not is_uniformly_continuous(f, x_sym, a)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f is continuous on [a, infinity)",
    "¬Q: f is not uniformly continuous on [a, infinity)"
]
N_HYP = 1
NEG_Q_INDEX = 1