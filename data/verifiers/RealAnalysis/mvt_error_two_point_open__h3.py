import sympy as sp
import math
from sympy.abc import x

N_HYP = 2
NEG_Q_INDEX = 2

CONDITION_LABELS = [
    "H_1: f is a real-valued function that is twice differentiable on the interval",
    "H_2: f second derivative is continuous on the interval",
    "¬Q: There does not exist c in the interval satisfying the error equation"
]

def conditions(witness):
    try:
        if len(witness) == 3:
            f_expr, a_expr, b_expr = witness
            a = float(sp.sympify(a_expr).evalf())
            b = float(sp.sympify(b_expr).evalf())
            h = (b - a) / 3.0
        elif len(witness) == 4:
            f_expr, a_expr, b_expr, h_expr = witness
            a = float(sp.sympify(a_expr).evalf())
            b = float(sp.sympify(b_expr).evalf())
            h = float(sp.sympify(h_expr).evalf())
        else:
            return [False, False, False]
        
        f = sp.sympify(f_expr)
        if len(f.free_symbols - {x}) > 0:
            return [False, False, False]
            
        f1 = sp.diff(f, x)
        f2 = sp.diff(f1, x)
    except Exception:
        return [False, False, False]

    try:
        t_min = min(a, b)
        t_max = max(a, b)
        if t_min == t_max:
            grid = [t_min]
        else:
            grid = [t_min + i * (t_max - t_min) / 100.0 for i in range(101)]
            
        h1_ok = True
        for t in grid:
            v0 = complex(f.subs(x, t).evalf())
            v1 = complex(f1.subs(x, t).evalf())
            v2 = complex(f2.subs(x, t).evalf())
            if math.isnan(v0.real) or math.isnan(v1.real) or math.isnan(v2.real):
                h1_ok = False
                break
            if abs(v0.imag) > 1e-7 or abs(v1.imag) > 1e-7 or abs(v2.imag) > 1e-7:
                h1_ok = False
                break
                
        h2_ok = h1_ok
    except Exception:
        h1_ok = False
        h2_ok = False

    if not (h1_ok and h2_ok):
        return [False, False, False]

    try:
        if a >= b:
            c_exists = False
        else:
            integral_val = sp.integrate(f, (x, a, b))
            integral_val = complex(integral_val.evalf()).real
            
            v_h1 = complex(f.subs(x, a + h).evalf()).real
            v_h2 = complex(f.subs(x, a + 2*h).evalf()).real
            approx_val = 1.5 * h * (v_h1 + v_h2)
            
            error = integral_val - approx_val
            
            inner_grid = [a + i * (b - a) / 1000.0 for i in range(1, 1000)]
            inner_f2_vals = []
            for t in inner_grid:
                val = complex(f2.subs(x, t).evalf())
                if abs(val.imag) <= 1e-7 and not math.isnan(val.real):
                    inner_f2_vals.append(val.real)
            
            if not inner_f2_vals:
                c_exists = False
            else:
                min_inner = min(inner_f2_vals)
                max_inner = max(inner_f2_vals)
                tol = 1e-5
                
                if abs(h) < 1e-12:
                    if abs(error) < 1e-9:
                        c_exists = True
                    else:
                        c_exists = False
                else:
                    target = error / (0.75 * h**3)
                    if min_inner - tol <= target <= max_inner + tol:
                        c_exists = True
                    else:
                        c_exists = False
                        
        neg_q = not c_exists
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]