import sympy as sp
import math

# Top-level setup
t = sp.Symbol('t', real=True)
x = sp.Symbol('x', real=True)
xs = sp.symbols('x1:11', real=True)
x1, x2, x3, x4, x5, x6, x7, x8, x9, x10 = xs

def make_callable(e, var_sym):
    if callable(e):
        return e
    return sp.lambdify(var_sym, e, modules=['math'])

def get_variation(expr, var_sym, N, a=0.0, b=1.0):
    is_vector_callable = False
    if callable(expr):
        try:
            test_val = expr(a + 1e-5)
            if isinstance(test_val, (list, tuple)):
                is_vector_callable = True
                funcs = [expr]
            else:
                funcs = [expr]
        except Exception:
            funcs = [expr]
    elif isinstance(expr, (list, tuple)):
        funcs = [make_callable(e, var_sym) for e in expr]
    else:
        funcs = [make_callable(expr, var_sym)]
        
    total_dist = 0.0
    prev_pt = None
    for i in range(N + 1):
        t_val = a + (b - a) * i / N
        # Avoid exact boundaries to prevent trivial division by zero
        if t_val == 0.0:
            t_val = 1e-10
        elif t_val == 1.0:
            t_val = 1.0 - 1e-10
            
        try:
            if is_vector_callable:
                pt = funcs[0](t_val)
                pt = [float(v) for v in pt]
            else:
                pt = [float(func(t_val)) for func in funcs]
        except Exception:
            try:
                if is_vector_callable:
                    pt = funcs[0](t_val + 1e-9)
                    pt = [float(v) for v in pt]
                else:
                    pt = [float(func(t_val + 1e-9)) for func in funcs]
            except Exception:
                return float('inf')
            
        if prev_pt is not None:
            dist = math.sqrt(sum((p - q)**2 for p, q in zip(pt, prev_pt)))
            total_dist += dist
        prev_pt = pt
    return total_dist

def is_rectifiable(expr, var_sym):
    v1000 = get_variation(expr, var_sym, 1000)
    v4000 = get_variation(expr, var_sym, 4000)
    v16000 = get_variation(expr, var_sym, 16000)
    
    if v16000 > 1e6 or math.isnan(v16000):
        return False
        
    diff1 = v4000 - v1000
    diff2 = v16000 - v4000
    
    # If the curve is rectifiable, the variation converges to a finite limit.
    # For divergent variation (e.g., t * sin(1/t)), diff2 will be roughly equal to or greater than diff1.
    if diff2 > 0.2 and diff2 > 0.5 * diff1:
        return False
        
    return True

def get_composed_callable(gamma, f):
    gamma_is_vector_callable = False
    if callable(gamma):
        try:
            test_val = gamma(0.5)
            if isinstance(test_val, (list, tuple)):
                gamma_is_vector_callable = True
        except Exception:
            pass

    if gamma_is_vector_callable:
        gamma_funcs = [gamma]
        try:
            num_vars = len(gamma(0.5))
        except Exception:
            num_vars = 1
    elif isinstance(gamma, (list, tuple)):
        gamma_funcs = [make_callable(g, t) for g in gamma]
        num_vars = len(gamma)
    else:
        gamma_funcs = [make_callable(gamma, t)]
        num_vars = 1

    if not isinstance(f, (list, tuple)):
        f_list = [f]
    else:
        f_list = f
        
    f_funcs = []
    for fi in f_list:
        if callable(fi):
            f_funcs.append(fi)
        else:
            if num_vars == 1:
                if x in fi.free_symbols:
                    f_funcs.append(sp.lambdify(x, fi, modules=['math']))
                elif x1 in fi.free_symbols:
                    f_funcs.append(sp.lambdify(x1, fi, modules=['math']))
                else:
                    f_funcs.append(sp.lambdify(x, fi, modules=['math']))
            else:
                f_funcs.append(sp.lambdify(xs[:num_vars], fi, modules=['math']))
                
    def comp_func(t_val):
        if gamma_is_vector_callable:
            g_vals = gamma_funcs[0](t_val)
        else:
            g_vals = [g(t_val) for g in gamma_funcs]
            
        return [fi(*g_vals) for fi in f_funcs]
        
    return comp_func

def conditions(witness):
    """
    witness: A tuple (gamma, f) where:
      - gamma is a sympy expression in `t`, a list of expressions, or a callable representing a curve.
      - f is a sympy expression in `x` (or `x1`, `x2`, etc.), a list of expressions, or a callable representing a mapping.
    """
    try:
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False]
        gamma, f = witness
    except Exception:
        return [False, False]
        
    # H_1: gamma is a rectifiable curve
    try:
        h1 = is_rectifiable(gamma, t)
    except Exception:
        h1 = False
        
    # ¬Q: The composed curve f o gamma is NOT rectifiable
    try:
        comp_expr = get_composed_callable(gamma, f)
        neg_q = not is_rectifiable(comp_expr, t)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: gamma is a rectifiable curve",
    "¬Q: f o gamma is not rectifiable"
]

N_HYP = 1
NEG_Q_INDEX = 1