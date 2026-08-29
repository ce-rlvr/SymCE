import sympy
import math

def get_callable(f):
    if callable(f):
        return f
    if hasattr(f, 'free_symbols'):
        syms = list(f.free_symbols)
        if len(syms) == 1:
            return sympy.lambdify(syms[0], f, modules=['math', 'sympy'])
        elif len(syms) == 0:
            val = float(f)
            return lambda x: val
    raise ValueError("Not a valid function")

def is_injective(f, a, b, N=2000):
    try:
        func = get_callable(f)
    except Exception:
        return False
        
    pts = [a + i * (b - a) / N for i in range(N + 1)]
    
    vals = []
    for x in pts:
        try:
            v = float(func(x))
            vals.append((v, x))
        except Exception:
            pass
            
    if len(vals) < 2:
        return False
        
    vals.sort(key=lambda item: item[0])
    
    v_min = vals[0][0]
    v_max = vals[-1][0]
    v_range = v_max - v_min
    if v_range < 1e-9:
        return False
        
    v_tol = 1e-7 * v_range
    x_tol = 1e-2 * (b - a)
    
    for i in range(len(vals) - 1):
        v1, x1 = vals[i]
        v2, x2 = vals[i+1]
        if abs(v1 - v2) <= v_tol and abs(x1 - x2) >= x_tol:
            return False
            
    return True

def not_strictly_monotonic(f, a, b, N=2000):
    try:
        func = get_callable(f)
    except Exception:
        return False
        
    pts = [a + i * (b - a) / N for i in range(N + 1)]
    
    vals = []
    for x in pts:
        try:
            v = float(func(x))
            vals.append(v)
        except Exception:
            pass
            
    if len(vals) < 3:
        return False
        
    v_min = min(vals)
    v_max = max(vals)
    v_range = v_max - v_min
    if v_range < 1e-9:
        return True
        
    v_tol = 1e-9 * v_range
    
    is_inc = True
    is_dec = True
    has_flat = False
    
    for i in range(len(vals) - 1):
        diff = vals[i+1] - vals[i]
        if diff < -v_tol:
            is_inc = False
        if diff > v_tol:
            is_dec = False
        if abs(diff) <= v_tol:
            has_flat = True
            
    if is_inc and not has_flat:
        return False
    if is_dec and not has_flat:
        return False
        
    return True

def conditions(witness):
    try:
        f, a, b = witness
    except Exception:
        return [False, False]
        
    try:
        a = float(a)
        b = float(b)
    except Exception:
        return [False, False]
        
    if a >= b:
        return [False, False]
        
    try:
        h1 = is_injective(f, a, b)
    except Exception:
        h1 = False
        
    try:
        neg_q = not_strictly_monotonic(f, a, b)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f is an injective function on the interval",
    "¬Q: The function f is not strictly monotonic"
]

N_HYP = 1
NEG_Q_INDEX = 1