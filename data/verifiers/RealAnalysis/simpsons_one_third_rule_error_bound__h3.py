import sympy as sp
import math

x = sp.Symbol('x')

def conditions(witness):
    try:
        if len(witness) == 4:
            f_in, a_in, b_in, M_in = witness
            x_in = None
        elif len(witness) == 5:
            f_in, x_in, a_in, b_in, M_in = witness
        else:
            return [False, False, False]
            
        a = sp.sympify(a_in)
        b = sp.sympify(b_in)
        M = sp.sympify(M_in)
        
        a_f = float(a)
        b_f = float(b)
        M_f = float(M)
        
        if callable(f_in):
            var = sp.Symbol('x') if x_in is None else sp.sympify(x_in)
            f_expr = f_in(var)
        else:
            f_expr = sp.sympify(f_in)
            if x_in is not None:
                var = sp.sympify(x_in)
            else:
                free = f_expr.free_symbols
                var = list(free)[0] if free else sp.Symbol('x')
                
    except Exception:
        return [False, False, False]

    # H1: f is a real-valued function defined on the closed interval from a to b
    try:
        h1 = True
        if a_f >= b_f:
            h1 = False
        else:
            for i in range(11):
                val = a_f + (b_f - a_f) * i / 10.0
                ev = f_expr.subs(var, val).evalf()
                try:
                    ev_c = complex(ev)
                    if abs(ev_c.imag) > 1e-9 or math.isnan(ev_c.real) or math.isinf(ev_c.real):
                        h1 = False
                        break
                except Exception:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H2: f is four times continuously differentiable on the interval
    try:
        f4 = sp.diff(f_expr, var, 4)
        h2 = True
        for i in range(101):
            val = a_f + (b_f - a_f) * i / 100.0
            ev = f4.subs(var, val).evalf()
            try:
                ev_c = complex(ev)
                if abs(ev_c.imag) > 1e-9 or math.isnan(ev_c.real) or math.isinf(ev_c.real):
                    h2 = False
                    break
            except Exception:
                h2 = False
                break
    except Exception:
        h2 = False

    # neg_Q: The error bound inequality fails
    try:
        integral_val = sp.Integral(f_expr, (var, a_f, b_f)).evalf()
        mid = (a_f + b_f) / 2.0
        simpson_val = ((b_f - a_f) / 6.0 * (
            f_expr.subs(var, a_f) + 
            4 * f_expr.subs(var, mid) + 
            f_expr.subs(var, b_f)
        )).evalf()
        
        error = abs(complex(integral_val - simpson_val))
        bound = M_f * (b_f - a_f)**5 / 2880.0
        
        neg_q = error > bound + 1e-12
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a real-valued function defined on the closed interval from a to b",
    "H_2: f is four times continuously differentiable on the interval",
    "¬Q: The Simpson 1/3 rule error exceeds M(b-a)^5 / 2880"
]

N_HYP = 2
NEG_Q_INDEX = 2