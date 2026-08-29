import sympy
import math

x = sympy.Symbol('x', real=True, nonnegative=True)

def conditions(witness) -> list[bool]:
    try:
        if callable(witness):
            expr = witness(x)
        else:
            expr = witness
            
        syms = list(expr.free_symbols)
        if len(syms) == 1:
            sym = syms[0]
        elif len(syms) == 0:
            sym = x
        else:
            sym = x
    except Exception:
        return [False, False, False]

    try:
        h1 = True
        for val in [0.0, 0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 100.0, 1000.0]:
            v = float(expr.subs(sym, val))
            if math.isinf(v) or math.isnan(v) or v < -1e-9:
                h1 = False
                break
    except Exception:
        h1 = False

    try:
        t = sympy.Symbol('t', real=True, nonnegative=True)
        expr_t = expr.subs(sym, t)
        try:
            int1 = sympy.integrate(expr_t, (t, 0, 1.0))
            val1 = float(int1)
            if math.isinf(val1) or math.isnan(val1):
                h2 = False
            else:
                h2 = True
        except Exception:
            n_steps = 100
            dx = 1.0 / n_steps
            val1 = sum(float(expr_t.subs(t, (i + 0.5) * dx)) * dx for i in range(n_steps))
            if math.isinf(val1) or math.isnan(val1):
                h2 = False
            else:
                h2 = True
    except Exception:
        h2 = False

    try:
        neg_q = False
        t = sympy.Symbol('t', real=True, nonnegative=True)
        expr_t = expr.subs(sym, t)
        
        indef_int = sympy.integrate(expr_t, t)
        
        for val in [0.1, 0.5, 1.0, 2.0, 5.0, 10.0]:
            try:
                integral_val = indef_int.subs(t, val) - indef_int.subs(t, 0)
                integral_num = float(integral_val)
            except Exception:
                try:
                    integral_val = sympy.integrate(expr_t, (t, 0, val))
                    integral_num = float(integral_val)
                except Exception:
                    n_steps = 1000
                    dx = val / n_steps
                    integral_num = sum(float(expr_t.subs(t, (i + 0.5) * dx)) * dx for i in range(n_steps))
            
            fx = float(expr_t.subs(t, val))
            rhs = val * fx
            
            if integral_num < rhs - 1e-9:
                neg_q = True
                break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a non-negative real-valued function defined on 0 to infinity",
    "H_2: f is Riemann integrable on 0 to x for every x > 0",
    "not_Q: There exists x > 0 such that integral from 0 to x of f(t) dt < x f(x)"
]

N_HYP = 2
NEG_Q_INDEX = 2