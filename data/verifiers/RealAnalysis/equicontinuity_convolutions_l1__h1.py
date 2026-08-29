import sympy as sp
from sympy import Symbol, S, integrate, oo, diff, limit, Abs, sin, cos, pi, Piecewise, Heaviside, sign, floor, ceiling, DiracDelta
import math

# Top-level setup
x = Symbol('x', real=True)
t = Symbol('t', real=True)
n = Symbol('n', integer=True)

MATH_MODULES = [
    'math',
    {
        'sign': lambda x: 1 if x > 0 else (-1 if x < 0 else 0),
        'Heaviside': lambda x: 1 if x >= 0 else 0,
        'Abs': abs,
        'Min': min,
        'Max': max
    }
]

def get_max_in_range(f_lam, start, end, steps):
    m = 0
    step = (end - start) / steps
    for i in range(steps + 1):
        x_val = start + i * step
        try:
            val = f_lam(x_val)
            if isinstance(val, complex):
                if val.imag != 0:
                    continue
                val = val.real
            v = abs(val)
            if v > m: 
                m = v
        except Exception:
            pass
    return m

def is_bounded_function(expr, var):
    try:
        f_lam = sp.lambdify(var, expr, modules=MATH_MODULES)
        m0 = get_max_in_range(f_lam, -1, 1, 2000)
        m1 = get_max_in_range(f_lam, -10, 10, 200)
        m2 = get_max_in_range(f_lam, 1000, 1010, 200)
        m3 = get_max_in_range(f_lam, -1010, -1000, 200)
        
        if m0 > 1e5 or m1 > 1e5 or m2 > 1e5 or m3 > 1e5:
            return False
            
        max_large = max(m2, m3)
        if max_large > 100 and max_large > 5 * (m1 + 1):
            return False
        return True
    except Exception:
        return True

def is_continuous(expr, var):
    try:
        from sympy.calculus.util import continuous_domain
        dom = continuous_domain(expr, var, S.Reals)
        return dom == S.Reals
    except Exception:
        if expr.has(Heaviside, sign, floor, ceiling, DiracDelta):
            return False
        return True

def compute_h(f_expr, g_expr, var_x, var_t):
    try:
        integrand = f_expr.subs(var_x, var_x - var_t) * g_expr
        h = sp.integrate(integrand, (var_t, -sp.oo, sp.oo))
        if h.has(sp.Integral) or h.has(sp.oo) or h.has(-sp.oo) or h.has(sp.nan):
            return None
        return h
    except Exception:
        return None

def check_H1(f_expr, var_x, var_n, is_param):
    if not is_param:
        df = sp.diff(f_expr, var_x)
        return is_bounded_function(df, var_x)
    else:
        max_derivs = []
        for n_val in [1, 5, 10, 20]:
            df = sp.diff(f_expr.subs(var_n, n_val), var_x)
            if not is_bounded_function(df, var_x):
                return False
            try:
                f_lam = sp.lambdify(var_x, df, modules=MATH_MODULES)
                m = get_max_in_range(f_lam, -10, 10, 200)
                max_derivs.append(m)
            except Exception:
                pass
        if len(max_derivs) >= 2:
            if max_derivs[-1] > max_derivs[0] * 5 and max_derivs[-1] > 10:
                return False
        return True

def check_H2(f_expr, var_x, var_n, is_param):
    if not is_param:
        return is_bounded_function(f_expr, var_x)
    else:
        max_vals = []
        for n_val in [1, 5, 10, 20]:
            f_n = f_expr.subs(var_n, n_val)
            if not is_bounded_function(f_n, var_x):
                return False
            try:
                f_lam = sp.lambdify(var_x, f_n, modules=MATH_MODULES)
                m = get_max_in_range(f_lam, -10, 10, 200)
                max_vals.append(m)
            except Exception:
                pass
        if len(max_vals) >= 2:
            if max_vals[-1] > max_vals[0] * 5 and max_vals[-1] > 10:
                return False
        return True

def check_H3(f_expr, g_expr, var_x, var_t, var_n, is_param):
    if not is_param:
        h = compute_h(f_expr, g_expr, var_x, var_t)
        return h is not None
    else:
        for n_val in [1, 2]:
            f_n = f_expr.subs(var_n, n_val)
            h = compute_h(f_n, g_expr, var_x, var_t)
            if h is None:
                return False
        return True

def check_neg_Q(f_expr, g_expr, var_x, var_t, var_n, is_param):
    if not is_param:
        h = compute_h(f_expr, g_expr, var_x, var_t)
        if h is None:
            return False
        if not is_continuous(h, var_x):
            return True
        dh = sp.diff(h, var_x)
        return not is_bounded_function(dh, var_x)
    else:
        max_derivs = []
        for n_val in [1, 5, 10, 20]:
            f_n = f_expr.subs(var_n, n_val)
            h = compute_h(f_n, g_expr, var_x, var_t)
            if h is None:
                continue
            if not is_continuous(h, var_x):
                return True
            dh = sp.diff(h, var_x)
            if not is_bounded_function(dh, var_x):
                return True
            try:
                f_lam = sp.lambdify(var_x, dh, modules=MATH_MODULES)
                m = get_max_in_range(f_lam, -10, 10, 200)
                max_derivs.append(m)
            except Exception:
                pass
        if len(max_derivs) >= 2:
            if max_derivs[-1] > max_derivs[0] * 2 and max_derivs[-1] > 5:
                return True
        return False

def conditions(witness) -> list[bool]:
    if not isinstance(witness, dict):
        return [False, False, False, False]
        
    var_x = witness.get('x', x)
    var_t = witness.get('t', t)
    var_n = witness.get('n', n)
    
    f_input = witness.get('f')
    g_expr = witness.get('g')
    
    if f_input is None or g_expr is None:
        return [False, False, False, False]
        
    is_param = False
    if isinstance(f_input, list):
        if not f_input:
            return [False, False, False, False]
        f_expr = f_input[0]
    else:
        f_expr = f_input
        if var_n in f_expr.free_symbols:
            is_param = True

    try:
        h1 = bool(check_H1(f_expr, var_x, var_n, is_param))
    except Exception:
        h1 = False

    try:
        h2 = bool(check_H2(f_expr, var_x, var_n, is_param))
    except Exception:
        h2 = False

    try:
        h3 = bool(check_H3(f_expr, g_expr, var_x, var_t, var_n, is_param))
    except Exception:
        h3 = False

    try:
        nq = bool(check_neg_Q(f_expr, g_expr, var_x, var_t, var_n, is_param))
    except Exception:
        nq = False

    return [h1, h2, h3, nq]

CONDITION_LABELS = [
    "H_1: F is an equicontinuous family of real-valued functions on R",
    "H_2: F is uniformly bounded on R",
    "H_3: C is the family of convolutions (integrals converge everywhere)",
    "¬Q: C is NOT equicontinuous on R"
]

N_HYP = 3
NEG_Q_INDEX = 3