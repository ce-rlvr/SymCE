import sympy
from sympy import Symbol, limit, diff, S, oo
import itertools

# Top-level setup for witness expressions
x = Symbol('x', real=True)

def is_convex(f, interval, x_sym):
    a = interval.inf
    b = interval.sup
    
    # Check if endpoints are finite if closed
    if not interval.left_open and a.is_finite:
        try:
            fa = limit(f, x_sym, a, dir='+')
            if not fa.is_finite:
                return False
        except Exception:
            pass
    if not interval.right_open and b.is_finite:
        try:
            fb = limit(f, x_sym, b, dir='-')
            if not fb.is_finite:
                return False
        except Exception:
            pass
            
    # Generate test points in the interval
    points = []
    if a.is_finite and b.is_finite:
        w = b - a
        points = [a + w*S(i)/10 for i in range(11)]
    elif a.is_finite and not b.is_finite:
        points = [a + S(i) for i in range(11)]
    elif not a.is_finite and b.is_finite:
        points = [b - S(i) for i in range(11)]
    else:
        points = [S(i) for i in range(-5, 6)]
        
    t_vals = [S(1)/4, S(1)/2, S(3)/4]
    
    # Check convexity definition on grid
    for x1, x2 in itertools.combinations(points, 2):
        for t in t_vals:
            xm = t*x1 + (1-t)*x2
            
            try:
                val_m = f.subs(x_sym, xm).evalf()
                val_1 = f.subs(x_sym, x1).evalf()
                val_2 = f.subs(x_sym, x2).evalf()
                
                fm = float(val_m)
                f1 = float(val_1)
                f2 = float(val_2)
            except Exception:
                continue
                
            tol = 1e-4 * max(1.0, abs(fm))
            if fm > float(t)*f1 + float(1-t)*f2 + tol:
                return False
                
    # Check second derivative if possible
    try:
        f2 = diff(f, x_sym, 2)
        for p in points:
            if p == a and a.is_finite:
                p_eval = a + S(1)/1000
            elif p == b and b.is_finite:
                p_eval = b - S(1)/1000
            else:
                p_eval = p
            val = f2.subs(x_sym, p_eval).evalf()
            try:
                fv = float(val)
                if fv < -1e-4:
                    return False
            except Exception:
                pass
    except Exception:
        pass
        
    return True

def is_not_locally_lipschitz(f, interval, x_sym):
    a = interval.inf
    b = interval.sup
    
    # For convex functions, failure of local Lipschitz continuity 
    # can only occur at included boundary points where the derivative becomes unbounded.
    
    if not interval.left_open and a.is_finite:
        try:
            fa = limit(f, x_sym, a, dir='+')
            if fa.is_finite:
                dq = (f - fa) / (x_sym - a)
                L = limit(dq, x_sym, a, dir='+')
                if L == oo or L == -oo or L == S.ComplexInfinity:
                    return True
        except Exception:
            pass
            
    if not interval.right_open and b.is_finite:
        try:
            fb = limit(f, x_sym, b, dir='-')
            if fb.is_finite:
                dq = (f - fb) / (x_sym - b)
                L = limit(dq, x_sym, b, dir='-')
                if L == oo or L == -oo or L == S.ComplexInfinity:
                    return True
        except Exception:
            pass
            
    return False

def conditions(witness):
    """
    witness: tuple (f, I) where f is a sympy expression and I is a sympy Interval.
    """
    try:
        f, I = witness
    except Exception:
        return [False, False]
        
    try:
        free = f.free_symbols
        if len(free) == 1:
            x_sym = list(free)[0]
        elif len(free) == 0:
            x_sym = Symbol('x')
        else:
            return [False, False]
    except Exception:
        return [False, False]
        
    try:
        h1 = is_convex(f, I, x_sym)
    except Exception:
        h1 = False
        
    try:
        neg_q = is_not_locally_lipschitz(f, I, x_sym)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f is a convex function on I",
    "¬Q: f is not locally Lipschitz continuous on I"
]

N_HYP = 1
NEG_Q_INDEX = 1