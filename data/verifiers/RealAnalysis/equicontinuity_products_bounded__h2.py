import sympy as sp
import math

x, n, m = sp.symbols('x n m')

CONDITION_LABELS = [
    "H_1: X is a metric space",
    "H_2: F and G are uniformly bounded on X",
    "¬Q: The family of pointwise products H is not equicontinuous on X"
]

N_HYP = 2
NEG_Q_INDEX = 2

def is_uniformly_bounded(expr, domain):
    a, b = domain
    expr = expr.subs(m, n)
    
    def get_max(n_val):
        expr_n = expr.subs(n, n_val)
        f = sp.lambdify(x, expr_n, modules=['math', 'sympy'])
        grid = [a + (b - a) * i / 200.0 for i in range(201)]
        grid += [a + 1e-5, b - 1e-5, a + 1e-7, b - 1e-7]
        vals = []
        for xv in grid:
            if xv < a or xv > b: 
                continue
            try:
                v = float(f(xv))
                if not math.isnan(v):
                    vals.append(abs(v))
            except Exception:
                pass
        if not vals: 
            return float('inf')
        return max(vals)
        
    m1 = get_max(1)
    m10 = get_max(10)
    m100 = get_max(100)
    
    if any(mv == float('inf') for mv in [m1, m10, m100]):
        return False
        
    if m100 > 1e6:
        return False
        
    if m100 > 2 * m10 and m100 > 1e-2:
        return False
        
    return True

def is_not_equicontinuous(F_expr, G_expr, domain):
    a, b = domain
    H_expr = F_expr * G_expr.subs(m, n)
    
    dH = sp.diff(H_expr, x)
    
    def get_max_deriv(n_val):
        dH_n = dH.subs(n, n_val)
        f = sp.lambdify(x, dH_n, modules=['math', 'sympy'])
        grid = [a + (b - a) * i / 200.0 for i in range(201)]
        vals = []
        for xv in grid:
            try:
                v = float(f(xv))
                if not math.isnan(v):
                    vals.append(abs(v))
            except Exception:
                pass
        if not vals: 
            return float('inf')
        return max(vals)
        
    dm1 = get_max_deriv(1)
    dm10 = get_max_deriv(10)
    dm100 = get_max_deriv(100)
    
    def has_jumps(n_val):
        expr_n = H_expr.subs(n, n_val)
        f = sp.lambdify(x, expr_n, modules=['math', 'sympy'])
        grid = [a + (b - a) * i / 1000.0 for i in range(1001)]
        vals = []
        for xv in grid:
            try:
                v = float(f(xv))
                if not math.isnan(v):
                    vals.append(v)
                else:
                    vals.append(None)
            except Exception:
                vals.append(None)
        
        for i in range(len(vals) - 1):
            if vals[i] is not None and vals[i+1] is not None:
                if abs(vals[i] - vals[i+1]) > 0.5:
                    return True
        return False

    if has_jumps(1) or has_jumps(10) or has_jumps(100):
        return True

    if any(dm == float('inf') for dm in [dm1, dm10, dm100]):
        return True
        
    if dm100 > 2 * dm10 and dm100 > 5:
        return True
        
    if dm100 > 1e6:
        return True
        
    return False

def conditions(witness):
    try:
        F_expr, G_expr, domain = witness
        F_expr = sp.sympify(F_expr)
        G_expr = sp.sympify(G_expr)
    except Exception:
        return [False, False, False]
        
    # H_1: X is a metric space
    try:
        a, b = domain
        h1 = float(a) < float(b)
    except Exception:
        h1 = False
        
    # H_2: F and G are uniformly bounded on X
    try:
        h2 = is_uniformly_bounded(F_expr, domain) and is_uniformly_bounded(G_expr, domain)
    except Exception:
        h2 = False
        
    # neg_Q: H is NOT equicontinuous on X
    try:
        neg_q = is_not_equicontinuous(F_expr, G_expr, domain)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]