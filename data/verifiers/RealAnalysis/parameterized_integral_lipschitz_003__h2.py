import sympy as sp
import math

# Top-level setup: named object bindings that the witness expression may reference.
x, y, t = sp.symbols('x y t', real=True)

def conditions(witness) -> list[bool]:
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should be a dictionary with keys:
      'a', 'b': floats defining the interval [a, b]
      'X_min', 'X_max': floats defining the metric space X as an interval [X_min, X_max]
      'L': float > 0, the Lipschitz constant
      'f': a callable f(x, t) returning a sympy expression, or a sympy expression string
    """
    try:
        a = float(witness['a'])
        b = float(witness['b'])
        L = float(witness['L'])
        X_min = float(witness['X_min'])
        X_max = float(witness['X_max'])
        f_val = witness['f']
    except Exception:
        return [False, False, False, False]
        
    try:
        if callable(f_val):
            f_expr = f_val(x, t)
        elif isinstance(f_val, str):
            f_expr = sp.sympify(f_val, locals={'x': x, 't': t})
        else:
            f_expr = f_val
    except Exception:
        return [False, False, False, False]
        
    # H_1: X is a metric space and [a,b] is a closed interval
    try:
        h1_ok = (a <= b) and (X_min <= X_max)
    except Exception:
        h1_ok = False
        
    # H_2: There exists L > 0 such that |f(x, t) - f(y, t)| <= L d_X(x, y)
    try:
        if L <= 0:
            h2_ok = False
        else:
            h2_ok = True
            try:
                f_lam = sp.lambdify((x, t), f_expr, modules=['math'])
                use_lam = True
            except Exception:
                use_lam = False
                
            x_vals = [X_min + i * (X_max - X_min) / 20 for i in range(21)]
            t_vals = [a + i * (b - a) / 20 for i in range(21)]
            
            for tv in t_vals:
                f_x_vals = []
                for xv in x_vals:
                    try:
                        if use_lam:
                            val = float(f_lam(xv, tv))
                        else:
                            val = float(f_expr.subs({x: xv, t: tv}).evalf())
                        f_x_vals.append(val)
                    except Exception:
                        try:
                            val = float(f_expr.subs({x: xv, t: tv}).evalf())
                            f_x_vals.append(val)
                        except Exception:
                            f_x_vals.append(None)
                
                for i in range(len(x_vals)):
                    for j in range(i+1, len(x_vals)):
                        if f_x_vals[i] is not None and f_x_vals[j] is not None:
                            dist = abs(f_x_vals[i] - f_x_vals[j])
                            x_dist = abs(x_vals[i] - x_vals[j])
                            if x_dist > 1e-9:
                                if dist > L * x_dist + 1e-4:
                                    h2_ok = False
                                    break
                        else:
                            h2_ok = False
                            break
                    if not h2_ok:
                        break
                if not h2_ok:
                    break
    except Exception:
        h2_ok = False
        
    # H_3: F(x) is defined by the integral F(x) = int_a^b f(x, t) dt
    try:
        F_expr = sp.integrate(f_expr, (t, a, b))
        h3_ok = True
    except Exception:
        h3_ok = False
        
    # ¬Q: F(x) is NOT globally Lipschitz continuous on X with constant L(b-a)
    try:
        if not h3_ok:
            neg_q = False
        else:
            is_lipschitz = True
            x_vals = [X_min + i * (X_max - X_min) / 20 for i in range(21)]
            F_vals = []
            
            try:
                F_lam = sp.lambdify(x, F_expr, modules=['math'])
                use_lam = True
            except Exception:
                use_lam = False
                
            for xv in x_vals:
                try:
                    if use_lam:
                        val = float(F_lam(xv))
                    else:
                        val = float(F_expr.subs(x, xv).evalf())
                    F_vals.append(val)
                except Exception:
                    try:
                        val = float(F_expr.subs(x, xv).evalf())
                        F_vals.append(val)
                    except Exception:
                        F_vals.append(None)
            
            for val in F_vals:
                if val is None or math.isnan(val) or math.isinf(val):
                    is_lipschitz = False
                    break
                    
            if is_lipschitz:
                for i in range(len(x_vals)):
                    for j in range(i+1, len(x_vals)):
                        dist = abs(F_vals[i] - F_vals[j])
                        x_dist = abs(x_vals[i] - x_vals[j])
                        if x_dist > 1e-9:
                            if dist > L * (b - a) * x_dist + 1e-4:
                                is_lipschitz = False
                                break
                    if not is_lipschitz:
                        break
            neg_q = not is_lipschitz
    except Exception:
        neg_q = False
        
    return [h1_ok, h2_ok, h3_ok, neg_q]

CONDITION_LABELS = [
    "H_1: X is a metric space and interval is closed",
    "H_2: f is Lipschitz continuous in x with constant L",
    "H_3: F is defined by the integral of f",
    "¬Q: F is not globally Lipschitz continuous with constant L times length of interval"
]

N_HYP = 3
NEG_Q_INDEX = 3