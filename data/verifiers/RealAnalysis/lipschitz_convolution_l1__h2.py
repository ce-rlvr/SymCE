import sympy
from sympy import S, Abs
from sympy.calculus.util import maximum, minimum

# Top-level setup for witness expressions
x = sympy.Symbol('x', real=True)
y = sympy.Symbol('y', real=True)

def is_lipschitz(f, var, L):
    try:
        if float(L) < 0:
            return False
    except Exception:
        pass

    try:
        df = sympy.diff(f, var)
    except Exception:
        return False
    
    # Analytical check
    try:
        max_val = maximum(df, var, S.Reals)
        min_val = minimum(df, var, S.Reals)
        if max_val <= L and min_val >= -L:
            return True
        if max_val > L or min_val < -L:
            return False
    except Exception:
        pass

    # Numerical fallback
    try:
        for val in range(-1000, 1000):
            v = val / 10.0
            df_v = df.subs(var, v)
            if abs(float(df_v)) > float(L) + 1e-7:
                return False
        return True
    except Exception:
        return False

def conclusion_fails(f, g, L, var):
    y_sym = sympy.Symbol('y', real=True)
    
    # 1. Check if norm_g is infinite
    try:
        norm_g = sympy.integrate(Abs(g), (var, -sympy.oo, sympy.oo))
        if norm_g == sympy.oo or norm_g == sympy.zoo or norm_g == sympy.nan or not norm_g.is_finite:
            if float(L) > 0:
                return True
    except Exception:
        pass

    # 2. Check limits of g at infinity (if it doesn't decay, it's not in L1)
    try:
        lim_inf = sympy.limit(g, var, sympy.oo)
        if lim_inf != 0:
            if float(L) > 0:
                return True
    except Exception:
        pass

    try:
        lim_minf = sympy.limit(g, var, -sympy.oo)
        if lim_minf != 0:
            if float(L) > 0:
                return True
    except Exception:
        pass

    # 3. Check if convolution is absolutely integrable at x=0
    try:
        abs_conv_at_0 = sympy.integrate(Abs(f.subs(var, -y_sym) * g.subs(var, y_sym)), (y_sym, -sympy.oo, sympy.oo))
        if abs_conv_at_0 == sympy.oo or abs_conv_at_0 == sympy.zoo or abs_conv_at_0 == sympy.nan or not abs_conv_at_0.is_finite:
            return True
    except Exception:
        pass

    # 4. Check if convolution is absolutely integrable at x=1
    try:
        abs_conv_at_1 = sympy.integrate(Abs(f.subs(var, 1-y_sym) * g.subs(var, y_sym)), (y_sym, -sympy.oo, sympy.oo))
        if abs_conv_at_1 == sympy.oo or abs_conv_at_1 == sympy.zoo or abs_conv_at_1 == sympy.nan or not abs_conv_at_1.is_finite:
            return True
    except Exception:
        pass

    # 5. If norm_g is finite, check if convolution derivative exceeds L * norm_g
    try:
        norm_g_val = sympy.integrate(Abs(g), (var, -sympy.oo, sympy.oo))
        if norm_g_val.is_finite:
            conv = sympy.integrate(f.subs(var, var-y_sym) * g.subs(var, y_sym), (y_sym, -sympy.oo, sympy.oo))
            if not conv.has(sympy.Integral):
                dconv = sympy.diff(conv, var)
                for val in range(-10, 11):
                    v = val / 2.0
                    try:
                        dconv_v = abs(float(dconv.subs(var, v)))
                        if dconv_v > float(L * norm_g_val) + 1e-7:
                            return True
                    except Exception:
                        # If derivative is undefined or infinite, it's not Lipschitz
                        return True
    except Exception:
        pass

    # 6. Numerical check for absolute convolution divergence at 0
    try:
        val_100 = 0.0
        for i in range(-100, 100):
            mid = i + 0.5
            val_100 += abs(float(f.subs(var, -mid) * g.subs(var, mid)))
            
        val_1000 = 0.0
        for i in range(-1000, 1000):
            mid = i + 0.5
            val_1000 += abs(float(f.subs(var, -mid) * g.subs(var, mid)))
            
        if val_1000 > val_100 + 50.0:
            return True
    except Exception:
        pass

    return False

def conditions(witness):
    try:
        f, g, L = witness
    except Exception:
        return [False, False]
    
    x_real = sympy.Symbol('x', real=True)
    
    try:
        if callable(f) and callable(g):
            f = f(x_real)
            g = g(x_real)
        else:
            free_vars = f.free_symbols | g.free_symbols
            if free_vars:
                var = None
                for v in free_vars:
                    if v.name == 'x':
                        var = v
                        break
                if var is None:
                    var = list(free_vars)[0]
                f = f.subs(var, x_real)
                g = g.subs(var, x_real)
    except Exception:
        pass
        
    var = x_real
    
    h1 = False
    try:
        h1 = is_lipschitz(f, var, L)
    except Exception:
        h1 = False
        
    neg_q = False
    try:
        neg_q = conclusion_fails(f, g, L, var)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f is globally Lipschitz continuous with constant L",
    "¬Q: The convolution f * g is not Lipschitz continuous with constant L ||g||_L1"
]

N_HYP = 1
NEG_Q_INDEX = 1