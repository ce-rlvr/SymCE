import sympy
import sympy.abc
import math

# Top-level setup
x, y, z = sympy.symbols('x y z')

def conditions(witness) -> list[bool]:
    try:
        f_expr = witness['f']
        g_expr = witness['g']
        a = float(witness['a'])
        b = float(witness['b'])
        c = float(witness['c'])
        d = float(witness['d'])
        var = witness.get('var', sympy.Symbol('x'))
    except Exception:
        return [False, False]

    def get_callable(func, var):
        if callable(func):
            return func
        if isinstance(func, str):
            func = sympy.sympify(func)
        return sympy.lambdify(var, func, modules=[{'Abs': math.fabs, 'sign': lambda x: 1 if x>0 else -1}, 'math', 'sympy'])

    try:
        g_call = get_callable(g_expr, var)
        f_call = get_callable(f_expr, var)
    except Exception:
        return [False, False]

    def h_call(x_val):
        return f_call(g_call(x_val))

    def evaluate_grid(func, a, b, n=100000):
        dx = (b - a) / n
        vals = []
        for i in range(n + 1):
            x_val = a + i * dx
            if x_val == 0:
                x_val += 1e-12
            try:
                v = float(func(x_val))
                if not math.isnan(v) and not math.isinf(v):
                    vals.append(v)
            except Exception:
                pass
        return vals

    h1_ok = False
    try:
        g_vals = evaluate_grid(g_call, a, b, 100000)
        if g_vals:
            min_g = min(g_vals)
            max_g = max(g_vals)
            if min_g >= c - 1e-4 and max_g <= d + 1e-4:
                tv_g = sum(abs(g_vals[i] - g_vals[i-1]) for i in range(1, len(g_vals)))
                range_g = max_g - min_g
                ratio_g = tv_g / range_g if range_g >= 1e-9 else 0
                max_jump_g = max((abs(g_vals[i] - g_vals[i-1]) for i in range(1, len(g_vals))), default=0)
                if ratio_g <= 5.0 and max_jump_g <= 0.5:
                    h1_ok = True
    except Exception:
        h1_ok = False

    neg_q = False
    try:
        h_vals = evaluate_grid(h_call, a, b, 100000)
        if h_vals:
            tv_h = sum(abs(h_vals[i] - h_vals[i-1]) for i in range(1, len(h_vals)))
            max_h = max(h_vals)
            min_h = min(h_vals)
            range_h = max_h - min_h
            ratio_h = tv_h / range_h if range_h >= 1e-9 else 0
            max_jump_h = max((abs(h_vals[i] - h_vals[i-1]) for i in range(1, len(h_vals))), default=0)
            if ratio_h > 5.0 or max_jump_h > 0.5:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: g is an absolutely continuous function",
    "¬Q: The composite function is not absolutely continuous"
]

N_HYP = 1
NEG_Q_INDEX = 1