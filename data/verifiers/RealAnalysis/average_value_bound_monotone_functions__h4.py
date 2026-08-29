import sympy as sp
import math

t = sp.Symbol('t')
x = sp.Symbol('x')

def conditions(witness):
    try:
        if len(witness) == 3:
            f, a, b = witness
            x_val = a
        elif len(witness) == 4:
            f, a, b, x_val = witness
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    if isinstance(f, str):
        try:
            f = sp.sympify(f)
        except Exception:
            pass

    if isinstance(f, sp.Expr):
        syms = list(f.free_symbols)
        if len(syms) == 1:
            var = syms[0]
            f_func = lambda val: float(f.subs(var, val))
            f_expr = f
        elif len(syms) == 0:
            var = sp.Symbol('t')
            f_func = lambda val: float(f)
            f_expr = f
        else:
            return [False, False, False, False]
    else:
        f_func_orig = f
        f_func = lambda val: float(f_func_orig(val))
        var = sp.Symbol('t')
        try:
            f_expr = f_func_orig(var)
        except Exception:
            f_expr = None

    try:
        a_f = float(a)
        b_f = float(b)
        x_f = float(x_val)
        if a_f > b_f:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: f is a real-valued function defined on the interval
    try:
        h1 = True
        if a_f == b_f:
            res = f_func(a_f)
            if res is None or not math.isfinite(res):
                h1 = False
        else:
            for i in range(101):
                val = a_f + i * (b_f - a_f) / 100.0
                res = f_func(val)
                if res is None or not math.isfinite(res):
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H_2: f is Riemann integrable on the interval
    try:
        h2 = False
        if f_expr is not None:
            try:
                integ = sp.integrate(f_expr, (var, a, b))
                if not integ.has(sp.oo, -sp.oo, sp.zoo, sp.nan):
                    h2 = True
            except Exception:
                pass
        
        if not h2:
            try:
                if a_f == b_f:
                    h2 = True
                else:
                    n_steps = 1000
                    dx = (b_f - a_f) / n_steps
                    total = sum(f_func(a_f + i*dx + dx/2) for i in range(n_steps)) * dx
                    if math.isfinite(total):
                        h2 = True
            except Exception:
                h2 = False
    except Exception:
        h2 = False

    # H_3: f is monotonically decreasing on the interval
    try:
        h3 = True
        if a_f == b_f:
            h3 = True
        else:
            pts = [a_f + i * (b_f - a_f) / 100.0 for i in range(101)]
            vals = [f_func(p) for p in pts]
            for i in range(len(vals)-1):
                if vals[i] < vals[i+1] - 1e-9:
                    h3 = False
                    break
    except Exception:
        h3 = False

    # not Q: f(x) <= 1/(x-a) \int_a^x f(t)dt FAILS
    try:
        if abs(x_f - a_f) < 1e-12:
            neg_q = True
        else:
            rhs = None
            if f_expr is not None:
                try:
                    integ = sp.integrate(f_expr, (var, a, x_val))
                    rhs = float(integ) / (x_f - a_f)
                except Exception:
                    pass
            
            if rhs is None:
                n_steps = 1000
                dx = (x_f - a_f) / n_steps
                total = sum(f_func(a_f + i*dx + dx/2) for i in range(n_steps)) * dx
                rhs = total / (x_f - a_f)
            
            lhs = f_func(x_f)
            if math.isnan(rhs) or math.isnan(lhs):
                neg_q = True
            elif lhs > rhs + 1e-9:
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = True

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: f is a real-valued function defined on the interval",
    "H_2: f is Riemann integrable on the interval",
    "H_3: f is monotonically decreasing on the interval",
    "not Q: conclusion fails"
]

N_HYP = 3
NEG_Q_INDEX = 3