import sympy
from sympy import Symbol, Piecewise, Ne, Eq, sin, cos, exp, log, pi
import math

# Top-level setup
x, y, z = sympy.symbols('x y z', real=True)

def check_callable(witness):
    f_eval = witness['f']
    a = witness.get('a', (0.0, 0.0))
    a_x, a_y = float(a[0]), float(a[1])
    
    h1 = True
    h2 = True
    
    # Asymmetric step sizes to correctly compute iterated limits at singularities
    h1_step = 1e-7
    k1_step = 1e-3
    
    def num_f_x(y_val):
        return (f_eval(a_x + h1_step, y_val) - f_eval(a_x - h1_step, y_val)) / (2 * h1_step)
    try:
        f_xy_a = (num_f_x(a_y + k1_step) - num_f_x(a_y - k1_step)) / (2 * k1_step)
    except Exception:
        return [h1, False, False, False]
        
    k2_step = 1e-7
    h2_step = 1e-3
    
    def num_f_y(x_val):
        return (f_eval(x_val, a_y + k2_step) - f_eval(x_val, a_y - k2_step)) / (2 * k2_step)
    try:
        f_yx_a = (num_f_y(a_x + h2_step) - num_f_y(a_x - h2_step)) / (2 * h2_step)
    except Exception:
        return [h1, False, False, False]
        
    def num_f_xy(px, py):
        step = 1e-5
        fx_plus = (f_eval(px + step, py + step) - f_eval(px - step, py + step)) / (2 * step)
        fx_minus = (f_eval(px + step, py - step) - f_eval(px - step, py - step)) / (2 * step)
        return (fx_plus - fx_minus) / (2 * step)
        
    def num_f_yx(px, py):
        step = 1e-5
        fy_plus = (f_eval(px + step, py + step) - f_eval(px + step, py - step)) / (2 * step)
        fy_minus = (f_eval(px - step, py + step) - f_eval(px - step, py - step)) / (2 * step)
        return (fy_plus - fy_minus) / (2 * step)
        
    h3 = True
    for dx, dy in [(1e-4, 1e-4), (1e-4, -1e-4), (-1e-4, 1e-4), (-1e-4, -1e-4)]:
        try:
            val_xy = num_f_xy(a_x + dx, a_y + dy)
            if abs(val_xy - f_xy_a) > 1e-2:
                h3 = False
            val_yx = num_f_yx(a_x + dx, a_y + dy)
            if abs(val_yx - f_yx_a) > 1e-2:
                h3 = False
        except Exception:
            h3 = False
            
    neg_q = abs(f_xy_a - f_yx_a) > 1e-3
    
    return [h1, h2, h3, neg_q]

def check_sympy(f_expr, vars, a):
    import sympy
    if len(vars) < 2:
        return [False, False, False, False]
        
    x_var, y_var = vars[0], vars[1]
    a_x, a_y = float(a[0]), float(a[1])
    
    h1 = True
    
    f_x = f_expr.diff(x_var)
    f_y = f_expr.diff(y_var)
    f_xy = f_x.diff(y_var)
    f_yx = f_y.diff(x_var)
    
    h2 = (f_xy != sympy.nan and f_yx != sympy.nan)
    
    f_eval = sympy.lambdify((x_var, y_var), f_expr, modules=['math', 'float'])
    
    def safe_f(xv, yv):
        try:
            return float(f_eval(xv, yv))
        except Exception:
            return float(f_expr.subs({x_var: xv, y_var: yv}))
            
    h1_step = 1e-7
    k1_step = 1e-3
    
    def num_f_x(y_val):
        return (safe_f(a_x + h1_step, y_val) - safe_f(a_x - h1_step, y_val)) / (2 * h1_step)
    try:
        f_xy_a = (num_f_x(a_y + k1_step) - num_f_x(a_y - k1_step)) / (2 * k1_step)
    except Exception:
        f_xy_a = None
        
    k2_step = 1e-7
    h2_step = 1e-3
    
    def num_f_y(x_val):
        return (safe_f(x_val, a_y + k2_step) - safe_f(x_val, a_y - k2_step)) / (2 * k2_step)
    try:
        f_yx_a = (num_f_y(a_x + h2_step) - num_f_y(a_x - h2_step)) / (2 * h2_step)
    except Exception:
        f_yx_a = None
        
    if f_xy_a is None or f_yx_a is None:
        return [h1, False, False, False]
        
    def check_cont(expr, val_a):
        for dx, dy in [(1e-4, 1e-4), (1e-4, -1e-4), (-1e-4, 1e-4), (-1e-4, -1e-4)]:
            try:
                val_near = float(expr.subs({x_var: a_x + dx, y_var: a_y + dy}).evalf())
                if abs(val_near - val_a) > 1e-2:
                    return False
            except Exception:
                return False
        return True
        
    h3 = check_cont(f_xy, f_xy_a) and check_cont(f_yx, f_yx_a)
    
    neg_q = abs(f_xy_a - f_yx_a) > 1e-3
    
    return [h1, h2, h3, neg_q]

def conditions(witness):
    try:
        if isinstance(witness, dict):
            f = witness['f']
            a = witness.get('a', (0.0, 0.0))
            if callable(f):
                return check_callable(witness)
            else:
                vars = witness.get('vars', tuple(sorted(f.free_symbols, key=lambda s: s.name)))
                return check_sympy(f, vars, a)
        elif callable(witness):
            return check_callable({'f': witness, 'a': (0.0, 0.0)})
        else:
            f = witness
            vars = tuple(sorted(f.free_symbols, key=lambda s: s.name))
            return check_sympy(f, vars, (0.0, 0.0))
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: U is an open set",
    "H_2: The second-order partial derivatives exist on U",
    "H_3: The mixed partial derivatives are continuous at a",
    "¬Q: The mixed partial derivatives are NOT equal at a"
]

N_HYP = 3
NEG_Q_INDEX = 3