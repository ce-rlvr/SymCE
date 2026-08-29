import sympy as sp
from sympy import S
from sympy.calculus.util import continuous_domain

# Top-level setup
x = sp.Symbol('x')

def sample_set(K, n=100):
    points = []
    if K.is_Union:
        args = K.args
    else:
        args = [K]
    for arg in args:
        if arg.is_Interval:
            start = float(arg.start) if arg.start != -sp.oo else -10.0
            end = float(arg.end) if arg.end != sp.oo else 10.0
            
            eps = 1e-5
            if arg.left_open: start += eps
            if arg.right_open: end -= eps
            
            if start > end: continue
            if start == end:
                points.append(start)
                continue
                
            for i in range(n):
                points.append(start + (end - start) * i / (n - 1))
        elif arg.is_FiniteSet:
            for p in arg.args:
                points.append(float(p))
    return points

def get_limit(f, x_sym, val, dir):
    try:
        if val == -sp.oo:
            return float(f.subs(x_sym, -1e6))
        elif val == sp.oo:
            return float(f.subs(x_sym, 1e6))
        else:
            eps = 1e-6
            if dir == '+':
                return float(f.subs(x_sym, float(val) + eps))
            else:
                return float(f.subs(x_sym, float(val) - eps))
    except Exception:
        return None

def is_continuous(K, f, x_sym):
    try:
        cd = continuous_domain(f, x_sym, S.Reals)
        if K.is_subset(cd) == S.true:
            return True
    except Exception:
        pass
        
    try:
        if K.is_Union:
            intervals = K.args
        elif K.is_Interval or K.is_FiniteSet:
            intervals = [K]
        else:
            return False
            
        for interval in intervals:
            if interval.is_FiniteSet:
                continue
            if not interval.is_Interval:
                continue
            pts = sample_set(interval, 50)
            for p in pts:
                val = float(f.subs(x_sym, p))
                if p > float(interval.start) + 1e-5:
                    val_left = float(f.subs(x_sym, p - 1e-5))
                    if abs(val - val_left) > 1e-2:
                        return False
                if p < float(interval.end) - 1e-5:
                    val_right = float(f.subs(x_sym, p + 1e-5))
                    if abs(val - val_right) > 1e-2:
                        return False
        return True
    except Exception:
        return False

def is_injective(K, f, x_sym):
    try:
        points = sample_set(K, 200)
        y_vals = []
        for p in points:
            try:
                y = float(f.subs(x_sym, p))
                y_vals.append((p, y))
            except Exception:
                pass
                
        y_vals.sort(key=lambda item: item[1])
        for i in range(len(y_vals)):
            p1, y1 = y_vals[i]
            for j in range(i+1, len(y_vals)):
                p2, y2 = y_vals[j]
                if abs(y1 - y2) >= 1e-3:
                    break
                if abs(p1 - p2) > 1e-2:
                    return False
        return True
    except Exception:
        return False

def check_inverse_discontinuous(K, f, x_sym):
    try:
        if K.is_Union:
            intervals = K.args
        elif K.is_Interval or K.is_FiniteSet:
            intervals = [K]
        else:
            return False
            
        images = []
        limits = []
        
        for interval in intervals:
            if interval.is_FiniteSet:
                for p in interval.args:
                    val = float(f.subs(x_sym, p))
                    images.append({
                        'min': val, 'max': val,
                        'min_inc': True, 'max_inc': True,
                        'x_min': float(p), 'x_max': float(p)
                    })
                    limits.append((float(p), val))
                continue
                
            if not interval.is_Interval:
                continue
                
            if interval.start == -sp.oo:
                y_start = get_limit(f, x_sym, -sp.oo, '+')
                start_inc = False
                x_start = -float('inf')
            else:
                y_start = get_limit(f, x_sym, interval.start, '+')
                start_inc = not interval.left_open
                x_start = float(interval.start)
                if start_inc:
                    try:
                        y_start = float(f.subs(x_sym, interval.start))
                    except Exception:
                        pass
                        
            if interval.end == sp.oo:
                y_end = get_limit(f, x_sym, sp.oo, '-')
                end_inc = False
                x_end = float('inf')
            else:
                y_end = get_limit(f, x_sym, interval.end, '-')
                end_inc = not interval.right_open
                x_end = float(interval.end)
                if end_inc:
                    try:
                        y_end = float(f.subs(x_sym, interval.end))
                    except Exception:
                        pass
                        
            if y_start is None or y_end is None:
                continue
                
            limits.append((x_start, y_start))
            limits.append((x_end, y_end))
            
            if y_start <= y_end:
                images.append({
                    'min': y_start, 'max': y_end,
                    'min_inc': start_inc, 'max_inc': end_inc,
                    'x_min': x_start, 'x_max': x_end
                })
            else:
                images.append({
                    'min': y_end, 'max': y_start,
                    'min_inc': end_inc, 'max_inc': start_inc,
                    'x_min': x_end, 'x_max': x_start
                })
                
        for b, L in limits:
            if b == float('inf') or b == -float('inf'):
                continue
                
            for img in images:
                y_min = img['min']
                y_max = img['max']
                
                if y_min + 1e-5 < L < y_max - 1e-5:
                    return True
                    
                if abs(L - y_min) <= 1e-5 and img['min_inc']:
                    x_0 = img['x_min']
                    if abs(x_0 - b) > 1e-4:
                        return True
                        
                if abs(L - y_max) <= 1e-5 and img['max_inc']:
                    x_0 = img['x_max']
                    if abs(x_0 - b) > 1e-4:
                        return True
                        
        return False
    except Exception:
        return False

def conditions(witness):
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    The witness is expected to be a tuple (K, f) or (K, f, x) where:
      - K is a sympy Set (e.g., Union of Intervals)
      - f is a sympy Expr or a callable
      - x is the sympy Symbol used in f (optional if f is callable or has 1 free symbol)
    """
    try:
        if len(witness) == 3:
            K, f, x_sym = witness
        elif len(witness) == 2:
            K, f = witness
            if callable(f):
                x_sym = sp.Symbol('x')
                f = f(x_sym)
            else:
                free_symbols = f.free_symbols
                if len(free_symbols) == 1:
                    x_sym = list(free_symbols)[0]
                elif len(free_symbols) == 0:
                    x_sym = sp.Symbol('x')
                else:
                    return [False, False, False]
        else:
            return [False, False, False]
            
        h1 = is_continuous(K, f, x_sym)
        h2 = is_injective(K, f, x_sym)
        neg_q = check_inverse_discontinuous(K, f, x_sym)
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: f is continuous on K",
    "H_2: f is injective on K",
    "¬Q: f^{-1} is not continuous on f(K)"
]

N_HYP = 2
NEG_Q_INDEX = 2